"""
I2C Timing Analysis Test

Measures actual blocking time for:
1. OLED display updates (worst case)
2. MCP4728 DAC updates (CV output)
3. Combined operation timing

This test will reveal if OLED updates can cause timing jitter in CV output.
"""

import time
import board
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107
import adafruit_mcp4728
import supervisor

# Setup LED for visual feedback
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("\n" + "="*60)
print("I2C TIMING ANALYSIS TEST")
print("="*60)

# Initialize I2C bus
displayio.release_displays()
time.sleep(0.2)
i2c = board.I2C()

# Initialize OLED
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = SH1107(display_bus, width=128, height=64)

# Initialize MCP4728
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
dac.wakeup()
time.sleep(0.1)
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.gain = 1
time.sleep(0.1)

# Setup display group
splash = displayio.Group()
display.root_group = splash

title = label.Label(terminalio.FONT, text="Timing Test", x=15, y=5, color=0xFFFFFF)
line1 = label.Label(terminalio.FONT, text="", x=5, y=25, color=0xFFFFFF)
line2 = label.Label(terminalio.FONT, text="", x=5, y=40, color=0xFFFFFF)
line3 = label.Label(terminalio.FONT, text="", x=5, y=55, color=0xFFFFFF)

splash.append(title)
splash.append(line1)
splash.append(line2)
splash.append(line3)

print("\n[TEST 1] MCP4728 DAC Update Time")
print("-" * 60)

# Test DAC update speed (critical path)
measurements = []
for i in range(100):
    start = supervisor.ticks_ms()
    dac.channel_a.raw_value = (i * 40) % 4096  # Different values
    end = supervisor.ticks_ms()
    elapsed = end - start
    measurements.append(elapsed)
    time.sleep(0.001)  # 1ms between updates

avg_dac = sum(measurements) / len(measurements)
max_dac = max(measurements)
min_dac = min(measurements)

print(f"  Average: {avg_dac:.2f} ms")
print(f"  Min:     {min_dac} ms")
print(f"  Max:     {max_dac} ms")
print(f"  Total for 100 updates: {sum(measurements):.2f} ms")

# Update display with results
line1.text = f"DAC: {avg_dac:.1f}ms avg"
line2.text = f"Max: {max_dac}ms"

print("\n[TEST 2] OLED Display Update Time")
print("-" * 60)

# Test display update speed (blocking operation)
measurements = []
for i in range(20):  # Fewer iterations (displays are slow)
    # Change display content
    title.text = f"Frame {i}"

    start = supervisor.ticks_ms()
    # Force display refresh by modifying and accessing
    display.refresh()
    end = supervisor.ticks_ms()

    elapsed = end - start
    measurements.append(elapsed)
    time.sleep(0.05)  # 50ms between updates

avg_display = sum(measurements) / len(measurements)
max_display = max(measurements)
min_display = min(measurements)

print(f"  Average: {avg_display:.2f} ms")
print(f"  Min:     {min_display} ms")
print(f"  Max:     {max_display} ms")
print(f"  Total for 20 updates: {sum(measurements):.2f} ms")

print("\n[TEST 3] Simulated Arpeggiator Loop")
print("-" * 60)
print("Simulating: Note change + Display update")

# Simulate worst case: note change + display update in same loop
measurements = []
for i in range(20):
    start = supervisor.ticks_ms()

    # Critical path: Update CV output
    midi_note = 36 + (i % 24)  # C2 to B3
    raw_value = int(midi_note * 68.27)
    dac.channel_a.raw_value = min(raw_value, 4095)

    # Non-critical: Update display
    line3.text = f"Note: {midi_note}"
    display.refresh()

    end = supervisor.ticks_ms()
    elapsed = end - start
    measurements.append(elapsed)

    led.value = not led.value
    time.sleep(0.1)

avg_combined = sum(measurements) / len(measurements)
max_combined = max(measurements)
min_combined = min(measurements)

print(f"  Average: {avg_combined:.2f} ms")
print(f"  Min:     {min_combined} ms")
print(f"  Max:     {max_combined} ms")

print("\n" + "="*60)
print("ANALYSIS")
print("="*60)

print("\nTiming Budget for Arpeggiator:")
print(f"  @ 120 BPM, 16th notes = {(60000 / 120 / 4):.1f} ms per note")
print(f"  @ 200 BPM, 16th notes = {(60000 / 200 / 4):.1f} ms per note")

print("\nWorst-Case Latency:")
print(f"  DAC only: {max_dac} ms")
print(f"  Display only: {max_display} ms")
print(f"  Combined: {max_combined} ms")

print("\nJitter Analysis:")
if max_dac - min_dac > 5:
    print(f"  ⚠️ DAC jitter: {max_dac - min_dac} ms (CONCERNING)")
else:
    print(f"  ✓ DAC jitter: {max_dac - min_dac} ms (acceptable)")

if max_display > 50:
    print(f"  ⚠️ Display blocking: {max_display} ms (BLOCKS AUDIO)")
else:
    print(f"  ✓ Display blocking: {max_display} ms (tolerable)")

print("\nRecommendations:")
if max_combined > 50:
    print("  ⚠️ CRITICAL: Display updates block CV output")
    print("  → Implement display throttling (update max 10Hz)")
    print("  → Separate display updates from note events")
    print("  → Consider display-free mode for live performance")
else:
    print("  ✓ Current I2C sharing acceptable")

print("\n" + "="*60)
print("Test complete. Review timing data above.")
print("="*60)

# Cleanup
led.value = False

# Keep display on with final results
while True:
    line1.text = f"DAC:{avg_dac:.1f}ms"
    line2.text = f"OLED:{avg_display:.1f}ms"
    line3.text = f"Both:{avg_combined:.1f}ms"
    time.sleep(1)
