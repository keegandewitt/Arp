"""
True S-Trig Transistor Test

Tests NPN transistor switching circuit for real S-Trig output.

Hardware Setup:
1. NPN transistor (2N3904 or 2N2222):
   - Emitter → Ground
   - Base → 1kΩ resistor → M4 D10
   - Collector → S-Trig output TIP

2. S-Trig output jack:
   - TIP: Transistor collector
   - SLEEVE: Ground

3. Multimeter (for verification):
   - Resistance mode (Ω)
   - Measure TIP to SLEEVE

Expected Behavior:
- GPIO LOW (0V): TIP is OPEN (floating, >10MΩ)
- GPIO HIGH (3.3V): TIP is SHORT to GND (<1Ω)

LED Pattern:
- ON: S-Trig ACTIVE (short to ground)
- OFF: S-Trig IDLE (open circuit)
"""

import time
import board
import digitalio

# Setup LED for visual feedback
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Setup D10 as S-Trig control GPIO
strig_gpio = digitalio.DigitalInOut(board.D10)
strig_gpio.direction = digitalio.Direction.OUTPUT

print("\n" + "="*60)
print("TRUE S-TRIG TRANSISTOR TEST")
print("="*60)
print("\nHardware Check:")
print("  1. NPN transistor installed (2N3904 or 2N2222)?")
print("  2. Base resistor (1kΩ) connected D10 → Base?")
print("  3. Emitter connected to Ground?")
print("  4. Collector connected to S-Trig output TIP?")
print("  5. Multimeter ready (resistance mode)?")
print("\n" + "="*60)
print("\nTest Pattern:")
print("  LED ON  = GPIO HIGH = S-Trig ACTIVE (short to GND)")
print("  LED OFF = GPIO LOW  = S-Trig IDLE (open circuit)")
print("\n" + "="*60)

# Start with S-Trig IDLE (open circuit)
strig_gpio.value = False  # GPIO LOW = transistor OFF = open circuit
led.value = False

print("\n[STARTING] S-Trig in IDLE state (open circuit)")
print("→ Multimeter should read: OPEN (OL or >10MΩ)\n")

time.sleep(3)

print("Beginning toggle test (1 second intervals)...")
print("Watch LED and multimeter!\n")

cycle_count = 0

try:
    while True:
        cycle_count += 1

        # ACTIVE: Short to ground
        print(f"[{cycle_count}] S-Trig ACTIVE (GPIO HIGH)")
        print("    → Multimeter should read: SHORT (<1Ω)")
        print("    → LED: ON")
        strig_gpio.value = True  # GPIO HIGH = transistor ON = short to GND
        led.value = True
        time.sleep(1.0)

        # IDLE: Open circuit
        print(f"[{cycle_count}] S-Trig IDLE (GPIO LOW)")
        print("    → Multimeter should read: OPEN (OL)")
        print("    → LED: OFF\n")
        strig_gpio.value = False  # GPIO LOW = transistor OFF = open circuit
        led.value = False
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n\n[!] Test stopped by user")
    strig_gpio.value = False  # Return to IDLE (open circuit)
    led.value = False
    print("[✓] S-Trig returned to IDLE state (open circuit)\n")
    print("Verification Checklist:")
    print("  ✓ Did multimeter alternate between OPEN and SHORT?")
    print("  ✓ Did LED sync with the measurements?")
    print("  ✓ In ACTIVE state, was resistance < 1Ω?")
    print("  ✓ In IDLE state, was circuit truly open (OL)?")
    print("\nIf all checks passed: Circuit is working correctly!")
    print("If any failed: Check wiring and transistor orientation\n")
