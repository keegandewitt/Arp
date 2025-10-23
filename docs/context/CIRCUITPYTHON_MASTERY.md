# CircuitPython Mastery Reference
**Last Updated:** 2025-10-23
**Purpose:** Comprehensive reference to prevent crashes and ensure robust CircuitPython code

---

## Table of Contents
1. [Critical Crash Prevention](#critical-crash-prevention)
2. [Memory Management](#memory-management)
3. [Safe Mode & Debugging](#safe-mode--debugging)
4. [MIDI Programming](#midi-programming)
5. [busio Module (I2C, SPI, UART)](#busio-module)
6. [SAMD51 Platform Specifics](#samd51-platform-specifics)
7. [Design Guidelines & Best Practices](#design-guidelines--best-practices)
8. [Common Pitfalls & Solutions](#common-pitfalls--solutions)

---

## Critical Crash Prevention

### The Golden Rules

**1. NEVER allocate objects in hot code paths (main loop)**
- Pre-allocate all objects in initialization
- Reuse buffers instead of creating new ones
- Use `struct.pack_into()` instead of `struct.pack()`

**2. Call `gc.collect()` strategically**
```python
import gc

def my_function():
    # Do work that creates temporary objects
    result = process_data()
    # Immediately collect garbage after function
    gc.collect()
    return result

# In main loop after major operations
while True:
    handle_midi()
    update_display()
    gc.collect()  # Periodic cleanup
    time.sleep(0.001)
```

**3. Avoid string manipulation in loops**
```python
# BAD - creates new strings on every iteration
while True:
    message = "BPM: " + str(bpm)  # Creates 2 new strings!
    display.show(message)

# GOOD - pre-allocate format string
message_template = "BPM: {}"
while True:
    message = message_template.format(bpm)  # Still creates string, but only one
    display.show(message)

# BETTER - update display object directly
while True:
    display.update_bpm(bpm)  # Display handles string internally
```

**4. Import modules at top, NEVER in functions**
```python
# BAD - imports in function create memory allocation every call
def generate_random():
    import random  # DON'T DO THIS
    return random.randint(0, 100)

# GOOD - import once at module level
import random

def generate_random():
    return random.randint(0, 100)
```

**5. Use context managers for hardware resources**
```python
# GOOD - automatic cleanup
with busio.I2C(SCL, SDA) as i2c:
    devices = i2c.scan()

# ACCEPTABLE - manual cleanup
i2c = busio.I2C(SCL, SDA)
try:
    devices = i2c.scan()
finally:
    i2c.deinit()
```

---

## Memory Management

### Understanding CircuitPython Memory

**RAM Structure:**
- **Heap**: Python objects, strings, lists, etc.
- **Stack**: Function call frames, local variables
- **Static**: CircuitPython interpreter and C libraries

**SAMD51 (Feather M4):**
- Total RAM: 192KB
- Typical heap: ~130KB after initialization
- Stack: Default ~8KB (adjustable)

### Memory Fragmentation Prevention

**Problem:** Free memory exists but not in contiguous blocks

**Solutions:**

**1. Allocate large objects early**
```python
# During initialization
large_buffer = bytearray(1024)  # Allocate when heap is fresh
display_bitmap = displayio.Bitmap(128, 64, 2)

# Later in code
# Reuse large_buffer instead of creating new ones
```

**2. Use functions to auto-free local variables**
```python
def process_midi_batch():
    # Local variables are freed when function returns
    note_list = [60, 64, 67, 72]
    processed = [n + 12 for n in note_list]
    return processed  # note_list becomes "phantom" object, will be collected

# After function returns, call gc
result = process_midi_batch()
gc.collect()  # Clears phantom objects immediately
```

**3. Avoid repeated reassignment**
```python
# BAD - creates new string each iteration
text = "BPM: "
while True:
    text = text + str(bpm)  # Old "text" stays in memory until GC

# GOOD - use label.text property (if display supports it)
label.text = f"BPM: {bpm}"  # Display library handles cleanup
```

**4. Monitor memory usage**
```python
import gc

# Check free memory
print(f"Free memory: {gc.mem_free()} bytes")

# Check allocation stats (more detailed)
import memorymonitor
alloc = memorymonitor.AllocationSize()
print(f"Allocated: {alloc.current_size()} bytes")
```

### Memory Allocation Strategies

**Use .mpy files:**
- Compiled library format uses 3-4x less RAM than .py
- Always use .mpy bundles from CircuitPython bundle

**Import order matters:**
```python
# Order imports by size (largest first)
import displayio  # Large module
import adafruit_midi  # Medium module
import time  # Small built-in

# This helps reduce fragmentation during startup
```

**Minimize imports:**
```python
# BAD - imports entire module
import adafruit_midi
msg = adafruit_midi.note_on.NoteOn(60, 100)

# GOOD - import only what you need
from adafruit_midi.note_on import NoteOn
msg = NoteOn(60, 100)
```

---

## Safe Mode & Debugging

### Safe Mode Reasons (Complete List)

**Internal Software Errors:**

| Reason | Cause | Fix |
|--------|-------|-----|
| **GC_ALLOC_OUTSIDE_VM** | Heap allocation when VM not running | CircuitPython bug - report to Adafruit |
| **FLASH_WRITE_FAIL** | Failed to write internal flash | Reflash firmware; test different board |
| **HARD_FAULT** | Memory access or instruction error (out-of-bounds) | Check array bounds; review pointer operations |
| **INTERRUPT_ERROR** | Error during interrupt handling | Simplify ISRs; reduce interrupt complexity |
| **NLR_JUMP_FAILED** | Exception handling failed (likely memory corruption) | Check for memory leaks; restart board |
| **NO_HEAP** | Unable to allocate heap at startup | Increase RAM; reduce loaded modules |
| **SDK_FATAL_ERROR** | Third-party firmware fatal error | Update SDK; check hardware compatibility |
| **WATCHDOG** | Internal watchdog timer expired | Optimize code; add breaks in loops |

**Hardware Failures:**
- **NO_CIRCUITPY**: Flash storage inaccessible - try reflash; replace board

**Power Issues:**
- **BROWNOUT**: Voltage dip - use better power supply; reduce peripheral load

**Stack Configuration:**
- **STACK_OVERFLOW**: Stack exceeded - use `supervisor.runtime.next_stack_limit`

**USB Configuration (boot.py):**
- **USB_TOO_MANY_ENDPOINTS**: Too many USB devices - reduce count
- **USB_TOO_MANY_INTERFACE_NAMES**: Too many interface names
- **USB_BOOT_DEVICE_NOT_INTERFACE_ZERO**: Boot device must be interface #0

**Programmatic:**
- **SAFE_MODE_PY_ERROR**: Error in safemode.py script
- **PROGRAMMATIC**: Triggered via `microcontroller.on_next_reset()`
- **USER**: Manual safe mode entry (hold RESET during boot)

### Diagnosing Crashes

**Check safe mode reason:**
```python
import supervisor

if supervisor.runtime.safe_mode_reason is not None:
    print(f"Safe mode: {supervisor.runtime.safe_mode_reason}")
```

**Common crash patterns:**

**1. Hard Fault (Memory Access Error)**
```python
# CAUSE: Array index out of bounds
notes = [60, 64, 67]
note = notes[5]  # Index 5 doesn't exist - CRASH

# FIX: Bounds checking
if index < len(notes):
    note = notes[index]
```

**2. Stack Overflow**
```python
# CAUSE: Deep recursion
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Deep recursion

fib = fibonacci(1000)  # CRASH - stack overflow

# FIX: Iterative approach or increase stack
supervisor.runtime.next_stack_limit = 16384  # In boot.py
```

**3. Memory Allocation Failure**
```python
# CAUSE: Allocating too much in loop
while True:
    data = bytearray(10000)  # Large allocation
    process(data)
    # Old 'data' not collected fast enough

# FIX: Pre-allocate and reuse
data = bytearray(10000)
while True:
    fill_data(data)
    process(data)
    gc.collect()
```

### Debugging Techniques

**Enable verbose output:**
```python
import supervisor
supervisor.runtime.autoreload = False  # Disable auto-reload during debug
```

**Print memory stats:**
```python
import gc
import micropython

# Memory info
gc.collect()
print(f"Free: {gc.mem_free()} bytes")
print(f"Allocated: {gc.mem_alloc()} bytes")

# Stack usage
micropython.stack_use()  # Prints current stack usage
```

**Safe mode serial output:**
When board enters safe mode, serial console shows:
```
Auto-reload is off.
Safe mode! HARD_FAULT
CircuitPython is in safe mode because you pressed the reset button during boot.
Press reset to exit safe mode.
```

---

## MIDI Programming

### USB MIDI vs UART MIDI

**USB MIDI (Built-in):**
```python
import usb_midi
import adafruit_midi

# USB MIDI ports (tuple of PortIn and PortOut)
usb_in = usb_midi.ports[0]   # First USB MIDI IN
usb_out = usb_midi.ports[1]  # First USB MIDI OUT

midi_usb = adafruit_midi.MIDI(midi_in=usb_in, midi_out=usb_out)
```

**UART MIDI (Hardware):**
```python
import board
import busio
import adafruit_midi

# UART at 31250 baud (MIDI standard)
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi_uart = adafruit_midi.MIDI(midi_in=uart, midi_out=uart)
```

### MIDI Message Handling

**Receiving messages:**
```python
msg = midi.receive()

if msg is not None:
    # Check message type
    if isinstance(msg, NoteOn):
        if msg.velocity > 0:
            print(f"Note On: {msg.note} velocity {msg.velocity}")
        else:
            # NoteOn with velocity 0 = NoteOff
            print(f"Note Off: {msg.note}")

    elif isinstance(msg, NoteOff):
        print(f"Note Off: {msg.note} velocity {msg.velocity}")

    elif isinstance(msg, ControlChange):
        print(f"CC#{msg.control} = {msg.value}")

    elif isinstance(msg, PitchBend):
        # 14-bit value: 0-16383 (8192 = no bend)
        print(f"Pitch Bend: {msg.pitch_bend}")
```

**Sending messages:**
```python
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

# Send single message
midi.send(NoteOn(60, 100))  # Middle C, velocity 100

# Send multiple messages (batch)
midi.send([
    NoteOn(60, 100),
    NoteOn(64, 100),
    NoteOn(67, 100)
])
```

**MIDI Clock messages:**
```python
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.midi_continue import Continue

# Clock ticks (24 PPQN - 24 per quarter note)
msg = midi.receive()
if isinstance(msg, TimingClock):
    # Clock tick received
    handle_clock_tick()

elif isinstance(msg, Start):
    # Start playback
    start_sequencer()

elif isinstance(msg, Stop):
    # Stop playback
    stop_sequencer()
```

### MIDI Channel Handling

**Channels are 0-indexed in library (0-15), but 1-16 in MIDI spec:**
```python
# Create MIDI on channel 1 (wire protocol: 0)
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=0,   # MIDI channel 1
    out_channel=0   # MIDI channel 1
)

# Listen to multiple channels
midi = adafruit_midi.MIDI(
    midi_in=uart,
    in_channel=(0, 1, 2),  # Channels 1, 2, 3
    out_channel=0
)
```

### MIDI Performance Tips

**1. Minimal latency - poll frequently:**
```python
# BAD - slow polling
while True:
    msg = midi.receive()
    process(msg)
    time.sleep(0.1)  # 100ms latency!

# GOOD - fast polling
while True:
    msg = midi.receive()
    if msg is not None:
        process(msg)
    time.sleep(0.001)  # 1ms latency
```

**2. Pass-through non-note messages immediately:**
```python
msg = midi.receive()
if msg is not None:
    if isinstance(msg, (NoteOn, NoteOff)):
        # Buffer for arpeggiator
        buffer_note(msg)
    else:
        # Pass through immediately (CC, pitch bend, etc.)
        midi.send(msg)
```

**3. Use timeout for UART:**
```python
# Short timeout prevents blocking
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
```

---

## busio Module

### I2C (Inter-Integrated Circuit)

**Initialization:**
```python
import busio
from board import SCL, SDA

i2c = busio.I2C(SCL, SDA, frequency=100000)  # 100kHz default
```

**Scanning for devices:**
```python
i2c.try_lock()
devices = i2c.scan()  # Returns list of addresses (0x08-0x77)
i2c.unlock()

print(f"Found devices: {[hex(addr) for addr in devices]}")
```

**Reading/Writing:**
```python
# Read from device
buffer = bytearray(4)
i2c.try_lock()
i2c.readfrom_into(0x3C, buffer)  # Read 4 bytes from address 0x3C
i2c.unlock()

# Write to device
data = bytes([0x00, 0x10, 0x20])
i2c.try_lock()
i2c.writeto(0x3C, data)
i2c.unlock()

# Write then read (common pattern)
i2c.try_lock()
i2c.writeto_then_readfrom(0x3C, bytes([0x00]), buffer)
i2c.unlock()
```

**CRITICAL: Always lock/unlock:**
```python
# Without locking - WILL CRASH
i2c.scan()  # ERROR!

# Correct usage
if i2c.try_lock():
    try:
        devices = i2c.scan()
    finally:
        i2c.unlock()
```

### UART (Serial Communication)

**Initialization:**
```python
uart = busio.UART(
    tx=board.TX,
    rx=board.RX,
    baudrate=9600,  # Bits per second
    bits=8,         # Data bits
    parity=None,    # Parity: None, UART.Parity.ODD, UART.Parity.EVEN
    stop=1,         # Stop bits: 1 or 2
    timeout=1.0,    # Read timeout in SECONDS (not ms!)
    receiver_buffer_size=64  # Input buffer size
)
```

**MIDI-specific UART:**
```python
# MIDI uses 31250 baud, 8N1
uart_midi = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
```

**Reading:**
```python
# Read up to N bytes (returns None on timeout)
data = uart.read(10)
if data is not None:
    print(f"Received: {data}")

# Read into buffer
buffer = bytearray(64)
count = uart.readinto(buffer)
if count is not None:
    print(f"Read {count} bytes")

# Read until newline
line = uart.readline()
```

**Writing:**
```python
# Write bytes
count = uart.write(b"Hello")
print(f"Sent {count} bytes")
```

**Check for data:**
```python
if uart.in_waiting > 0:
    data = uart.read(uart.in_waiting)
```

### SPI (Serial Peripheral Interface)

**Initialization:**
```python
spi = busio.SPI(
    clock=board.SCK,
    MOSI=board.MOSI,  # Master Out Slave In
    MISO=board.MISO   # Master In Slave Out
)
```

**Configuration:**
```python
spi.try_lock()
spi.configure(
    baudrate=100000,  # Clock speed in Hz
    polarity=0,       # Clock polarity (0 or 1)
    phase=0,          # Clock phase (0 or 1)
    bits=8            # Bits per transfer
)
spi.unlock()
```

**Transfer:**
```python
spi.try_lock()
try:
    # Write
    spi.write(bytes([0x01, 0x02, 0x03]))

    # Read
    buffer = bytearray(4)
    spi.readinto(buffer, write_value=0x00)  # Send 0x00 while reading

    # Full duplex (write and read simultaneously)
    out_buffer = bytes([0x01, 0x02])
    in_buffer = bytearray(2)
    spi.write_readinto(out_buffer, in_buffer)
finally:
    spi.unlock()
```

---

## SAMD51 Platform Specifics

### Feather M4 CAN Express

**Specs:**
- **MCU:** ATSAMD51J19 (ARM Cortex M4, 120MHz)
- **RAM:** 192KB
- **Flash:** 512KB
- **EEPROM:** None (use flash storage or QSPI)

**Pin Capabilities:**
- **Analog Inputs:** A0-A5 (12-bit ADC)
- **DAC Outputs:** A0, A1 (10-bit, 0-3.3V)
- **PWM:** Most digital pins
- **I2C:** One hardware I2C (D21/D22)
- **SPI:** One hardware SPI (MISO/MOSI/SCK)
- **UART:** Multiple UARTs available

**USB Endpoints:**
- SAMD51 provides 8 endpoint pairs
- Pair 0 reserved (control)
- 7 pairs available for USB devices
- USB MIDI + USB CDC + USB HID fits comfortably

### Power Management

**USB Power:**
- 5V from USB-C
- Max current: 500mA (USB 2.0 spec)
- Sufficient for M4 + FeatherWings

**Battery (LiPo):**
- Onboard charger: 500mA
- Voltage monitoring: `analogio.AnalogIn(board.VOLTAGE_MONITOR)`
- Battery voltage = reading * 2 (voltage divider)

**Low Power Mode:**
```python
import alarm

# Light sleep (CPU stops, peripherals run)
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 10)
alarm.light_sleep_until_alarms(time_alarm)

# Deep sleep (most things off)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
```

### SAMD51-Specific Issues

**SPI Baudrate Limitations:**
- SAMD51 can theoretically do 60MHz (half CPU clock)
- Practical max: 24MHz
- Use 12MHz or lower for reliability

**I2C Clock Stretching:**
- SAMD51 supports clock stretching
- Some devices need it (OLED displays)

**DAC Resolution:**
- 10-bit (0-1023)
- Output range: 0-3.3V
- Use op-amp for 0-5V or 0-10V

---

## Design Guidelines & Best Practices

### API Design

**Properties vs Methods:**
- **Properties:** Device state (temperature, voltage, switch position)
- **Methods:** Actions that cause changes (start, stop, send, configure)

```python
# Good design
class Arpeggiator:
    @property
    def bpm(self):
        """Current BPM (read-only)"""
        return self._bpm

    def start(self):
        """Start arpeggiator"""
        self.running = True
```

**Validation & Error Handling:**
```python
def set_bpm(self, bpm):
    """Set BPM with validation"""
    if not (40 <= bpm <= 240):
        raise ValueError("BPM must be 40-240")
    self._bpm = bpm
```

**Context Manager Support:**
```python
class HardwareResource:
    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

# Usage
with HardwareResource() as resource:
    resource.do_work()
# Automatically cleaned up
```

### Module Organization

**Small, focused modules:**
```
arp/
├── core/
│   ├── clock.py      # Clock handling only
│   ├── buffer.py     # Note buffer only
│   └── patterns.py   # Pattern generation only
├── ui/
│   ├── display.py    # Display management
│   └── buttons.py    # Button handling
└── utils/
    └── config.py     # Settings persistence
```

**Dependency injection:**
```python
# Good - accept configured objects
class ClockHandler:
    def __init__(self, midi_in_port):
        self.midi_clock = adafruit_midi.MIDI(midi_in=midi_in_port)

# Usage
clock = ClockHandler(usb_midi.ports[0])

# Bad - create dependencies internally
class ClockHandler:
    def __init__(self):
        import usb_midi
        self.midi_clock = adafruit_midi.MIDI(midi_in=usb_midi.ports[0])
```

### Constants

**Use const() for module-level constants:**
```python
from micropython import const

# Module constants (compile-time optimization)
_DEFAULT_BPM = const(120)
_MAX_NOTES = const(16)

# Class constants
class Settings:
    ARP_UP = const(0)
    ARP_DOWN = const(1)
```

---

## Common Pitfalls & Solutions

### 1. Infinite Loop Without Delay

**Problem:**
```python
# Watchdog will trigger - no time for other tasks
while True:
    process_data()
    # No delay!
```

**Solution:**
```python
while True:
    process_data()
    time.sleep(0.001)  # Give CPU a break
```

### 2. Forgotten deinit()

**Problem:**
```python
i2c = busio.I2C(SCL, SDA)
# Use i2c
# ... never call i2c.deinit()
# Pins remain claimed, can't be reused
```

**Solution:**
```python
# Use context manager
with busio.I2C(SCL, SDA) as i2c:
    i2c.scan()
# Automatically deinitialized

# Or manual
i2c = busio.I2C(SCL, SDA)
try:
    i2c.scan()
finally:
    i2c.deinit()
```

### 3. Importing in Functions

**Problem:**
```python
def get_random_pattern():
    import random  # Allocates memory EVERY call
    return random.choice(patterns)
```

**Solution:**
```python
import random  # Import once at module level

def get_random_pattern():
    return random.choice(patterns)
```

### 4. String Concatenation in Loops

**Problem:**
```python
# Creates TWO new strings per iteration
while True:
    label = "BPM: " + str(bpm)
    display.show(label)
```

**Solution:**
```python
# Use f-strings (still creates string, but more efficient)
while True:
    display.show(f"BPM: {bpm}")

# Or update display property directly
display.bpm_label.text = str(bpm)
```

### 5. Not Checking for None

**Problem:**
```python
msg = midi.receive()
note = msg.note  # CRASH if msg is None!
```

**Solution:**
```python
msg = midi.receive()
if msg is not None:
    if isinstance(msg, NoteOn):
        note = msg.note
```

### 6. Array Index Out of Bounds

**Problem:**
```python
notes = [60, 64, 67]
current_step = 0
while True:
    note = notes[current_step]  # Can crash if current_step >= len(notes)
    current_step += 1
```

**Solution:**
```python
notes = [60, 64, 67]
current_step = 0
while True:
    if notes:  # Check list not empty
        current_step = current_step % len(notes)  # Wrap around
        note = notes[current_step]
        current_step += 1
```

### 7. UART Timeout Units Confusion

**Problem:**
```python
# Timeout is in SECONDS, not milliseconds!
uart = busio.UART(TX, RX, baudrate=31250, timeout=1000)  # 1000 seconds!!
```

**Solution:**
```python
# Use seconds
uart = busio.UART(TX, RX, baudrate=31250, timeout=0.001)  # 1ms
```

### 8. Forgetting I2C/SPI Lock

**Problem:**
```python
i2c = busio.I2C(SCL, SDA)
devices = i2c.scan()  # CRASH - not locked!
```

**Solution:**
```python
i2c = busio.I2C(SCL, SDA)
if i2c.try_lock():
    try:
        devices = i2c.scan()
    finally:
        i2c.unlock()
```

---

## Quick Reference Cheat Sheet

### Memory Management
```python
import gc

# Check free memory
print(f"Free: {gc.mem_free()}")

# Force garbage collection
gc.collect()

# Pre-allocate buffers
buffer = bytearray(256)  # Reuse this

# Monitor allocations
import memorymonitor
alloc = memorymonitor.AllocationSize()
print(f"Allocated: {alloc.current_size()}")
```

### MIDI Essentials
```python
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Setup
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

# Receive
msg = midi.receive()
if msg is not None and isinstance(msg, NoteOn):
    print(f"Note: {msg.note}, Velocity: {msg.velocity}")

# Send
midi.send(NoteOn(60, 100))
```

### Hardware Resources
```python
# I2C
with busio.I2C(board.SCL, board.SDA) as i2c:
    if i2c.try_lock():
        devices = i2c.scan()
        i2c.unlock()

# UART (MIDI)
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)

# Always deinit or use context managers!
```

### Safe Mode Check
```python
import supervisor

if supervisor.runtime.safe_mode_reason:
    print(f"Crashed: {supervisor.runtime.safe_mode_reason}")
```

---

## Next Steps for Robust Code

1. **Audit all main loop allocations** - Move to initialization
2. **Add gc.collect() calls** - After major operations
3. **Pre-allocate buffers** - Reuse instead of recreate
4. **Use context managers** - Ensure cleanup
5. **Add bounds checking** - Prevent index errors
6. **Monitor memory** - Track usage during development
7. **Test on hardware** - Catch issues early

---

**Remember:** CircuitPython crashes are almost always memory-related or hardware access errors. Follow these guidelines and your code will be rock-solid.
