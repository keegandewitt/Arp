#!/usr/bin/env python3
"""
Generate COMPLETE BOARD SCHEMATICS - One per PCB
Session 25 - Shows ALL circuits on each board with proper organization
"""

import schemdraw
import schemdraw.elements as elm

# ============================================================================
# TOP BOARD COMPLETE - All Input Circuits
# ============================================================================

d_top = schemdraw.Drawing()

# Title
d_top += elm.Label().at((0, 18)).label('PRISME TOP BOARD - COMPLETE SCHEMATIC', fontsize=16, halign='left', font='bold')
d_top += elm.Label().at((0, 17.2)).label('Input Board: CV IN + TRIG IN protection circuits, LEDs, Power', fontsize=11, halign='left')
d_top += elm.Label().at((0, 16.6)).label('PCB Size: 90mm × 55mm | Date: 2025-11-03', fontsize=9, halign='left')

# ============================================================================
# SECTION 1: POWER RAILS (TOP BOARD)
# ============================================================================

d_top += elm.Label().at((0, 15.5)).label('POWER DISTRIBUTION', fontsize=13, halign='left', font='bold')

# 5V Rail
d_top += elm.Label().at((0, 14.5)).label('5V Rail (from M4 USB):', fontsize=10, halign='left', font='bold')
pwr_5v = (2, 14)
d_top += elm.Dot().at(pwr_5v).label('From M4\nUSB Pin', fontsize=9, halign='right')
d_top += elm.Line().right(1)
d_top += elm.Vdd().label('5V', fontsize=9)

# 5V decoupling
d_top += elm.Line().at((pwr_5v[0] + 1, pwr_5v[1])).down(0.5)
d_top += elm.Capacitor().down(1.2).label('C11\n10µF', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

d_top += elm.Line().at((pwr_5v[0] + 1, pwr_5v[1] - 0.5)).right(1.5)
d_top += elm.Capacitor().down(1.2).label('C12\n0.1µF', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# 3.3V Rail
d_top += elm.Label().at((6, 14.5)).label('3.3V Rail (from M4 3V3):', fontsize=10, halign='left', font='bold')
pwr_3v3 = (8.5, 14)
d_top += elm.Dot().at(pwr_3v3).label('From M4\n3V3 Pin', fontsize=9, halign='right')
d_top += elm.Line().right(1)
d_top += elm.Vdd().label('3.3V', fontsize=9)

# 3.3V decoupling
d_top += elm.Line().at((pwr_3v3[0] + 1, pwr_3v3[1])).down(0.5)
d_top += elm.Capacitor().down(1.2).label('C13\n10µF', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

d_top += elm.Line().at((pwr_3v3[0] + 1, pwr_3v3[1] - 0.5)).right(1.5)
d_top += elm.Capacitor().down(1.2).label('C14\n0.1µF', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# Power notes
d_top += elm.Label().at((0, 11.5)).label('Powers: LEDs, BAT85 clamp reference', fontsize=8, halign='left')

# ============================================================================
# SECTION 2: CV IN CIRCUIT
# ============================================================================

d_top += elm.Label().at((0, 10.5)).label('CV IN PROTECTION CIRCUIT', fontsize=13, halign='left', font='bold')

# Jack
cv_jack = (1, 9)
d_top += elm.Dot().at(cv_jack).label('CV IN\nJack TIP', fontsize=9, halign='right')

# Upper voltage divider resistor
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('R1 10kΩ', fontsize=8, loc='top')

# TAP point
cv_tap = (cv_jack[0] + 2.8, cv_jack[1])
d_top += elm.Dot().at(cv_tap).label('TAP', fontsize=8, loc='top')

# To M4 A3
d_top += elm.Line().at(cv_tap).right(2)
d_top += elm.Dot().label('To M4 A3\n(ADC)', fontsize=9, halign='left')

# Lower voltage divider resistor
d_top += elm.Line().at(cv_tap).down(0.8)
d_top += elm.Resistor().down(1.5).label('R2 10kΩ', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# BAT85 clamp to 3.3V
d_top += elm.Line().at(cv_tap).up(0.8)
d_top += elm.Diode().up(1.5).label('D1 BAT85', fontsize=8, loc='left')
d_top += elm.Line().up(0.3)
d_top += elm.Vdd().label('3.3V', fontsize=8)

# Optional smoothing cap
d_top += elm.Line().at((cv_tap[0] - 0.8, cv_tap[1])).down(0.8)
d_top += elm.Capacitor().down(1.5).label('C15\n100nF\n(opt)', fontsize=7, loc='left')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# Jack ground
d_top += elm.Line().at(cv_jack).down(0.8)
d_top += elm.Dot().label('Jack\nSLEEVE', fontsize=8, halign='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# CV LED indicator
cv_led_start = (cv_jack[0], cv_jack[1] - 2)
d_top += elm.Dot().at(cv_led_start).label('From M4 D4', fontsize=8, halign='right')
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('R3 1kΩ', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.LED().right(1.5).label('LED1\nWhite', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.Ground()

# ============================================================================
# SECTION 3: TRIG IN CIRCUIT
# ============================================================================

d_top += elm.Label().at((0, 4)).label('TRIG IN PROTECTION CIRCUIT', fontsize=13, halign='left', font='bold')

# Jack
trig_jack = (1, 2.5)
d_top += elm.Dot().at(trig_jack).label('TRIG IN\nJack TIP', fontsize=9, halign='right')

# Upper voltage divider resistor
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('R4 10kΩ', fontsize=8, loc='top')

# TAP point
trig_tap = (trig_jack[0] + 2.8, trig_jack[1])
d_top += elm.Dot().at(trig_tap).label('TAP', fontsize=8, loc='top')

# To M4 A4
d_top += elm.Line().at(trig_tap).right(2)
d_top += elm.Dot().label('To M4 A4\n(ADC)', fontsize=9, halign='left')

# Lower voltage divider resistor
d_top += elm.Line().at(trig_tap).down(0.8)
d_top += elm.Resistor().down(1.5).label('R5 10kΩ', fontsize=8, loc='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# BAT85 clamp to 3.3V
d_top += elm.Line().at(trig_tap).up(0.8)
d_top += elm.Diode().up(1.5).label('D2 BAT85', fontsize=8, loc='left')
d_top += elm.Line().up(0.3)
d_top += elm.Vdd().label('3.3V', fontsize=8)

# Optional smoothing cap
d_top += elm.Line().at((trig_tap[0] - 0.8, trig_tap[1])).down(0.8)
d_top += elm.Capacitor().down(1.5).label('C16\n100nF\n(opt)', fontsize=7, loc='left')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# Jack ground
d_top += elm.Line().at(trig_jack).down(0.8)
d_top += elm.Dot().label('Jack\nSLEEVE', fontsize=8, halign='right')
d_top += elm.Line().down(0.3)
d_top += elm.Ground()

# TRIG RGB LED (3 channels)
trig_led_r = (trig_jack[0], trig_jack[1] - 2)
d_top += elm.Dot().at(trig_led_r).label('M4 D11', fontsize=8, halign='right')
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('R6 330Ω', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.LED().right(1.5).label('LED2 R', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.Ground()

trig_led_g = (trig_jack[0], trig_jack[1] - 3)
d_top += elm.Dot().at(trig_led_g).label('M4 D23', fontsize=8, halign='right')
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('330Ω', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.LED().right(1.5).label('LED2 G', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.Ground()

trig_led_b = (trig_jack[0], trig_jack[1] - 4)
d_top += elm.Dot().at(trig_led_b).label('M4 D24', fontsize=8, halign='right')
d_top += elm.Line().right(0.8)
d_top += elm.Resistor().right(2).label('330Ω', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.LED().right(1.5).label('LED2 B', fontsize=8, loc='top')
d_top += elm.Line().right(0.5)
d_top += elm.Ground()

# ============================================================================
# SECTION 4: M4 CONNECTIONS SUMMARY
# ============================================================================

d_top += elm.Label().at((9, 10.5)).label('M4 CONNECTIONS', fontsize=12, halign='left', font='bold')
d_top += elm.Label().at((9, 10)).label('Power:', fontsize=10, halign='left', font='bold')
d_top += elm.Label().at((9, 9.6)).label('• USB → 5V Rail', fontsize=8, halign='left')
d_top += elm.Label().at((9, 9.2)).label('• 3V3 → 3.3V Rail', fontsize=8, halign='left')
d_top += elm.Label().at((9, 8.8)).label('• GND → Common GND', fontsize=8, halign='left')

d_top += elm.Label().at((9, 8.2)).label('ADC Inputs:', fontsize=10, halign='left', font='bold')
d_top += elm.Label().at((9, 7.8)).label('• A3 ← CV IN TAP', fontsize=8, halign='left')
d_top += elm.Label().at((9, 7.4)).label('• A4 ← TRIG IN TAP', fontsize=8, halign='left')

d_top += elm.Label().at((9, 6.8)).label('GPIO Outputs:', fontsize=10, halign='left', font='bold')
d_top += elm.Label().at((9, 6.4)).label('• D4 → LED1 (CV)', fontsize=8, halign='left')
d_top += elm.Label().at((9, 6)).label('• D11 → LED2 Red', fontsize=8, halign='left')
d_top += elm.Label().at((9, 5.6)).label('• D23 → LED2 Green', fontsize=8, halign='left')
d_top += elm.Label().at((9, 5.2)).label('• D24 → LED2 Blue', fontsize=8, halign='left')

# ============================================================================
# SECTION 5: COMPONENT VALUES
# ============================================================================

d_top += elm.Label().at((9, 3.5)).label('COMPONENT VALUES', fontsize=11, halign='left', font='bold')
d_top += elm.Label().at((9, 3.1)).label('Resistors:', fontsize=9, halign='left', font='bold')
d_top += elm.Label().at((9, 2.7)).label('R1,R2,R4,R5: 10kΩ 1/4W', fontsize=8, halign='left')
d_top += elm.Label().at((9, 2.3)).label('R3: 1kΩ 1/4W', fontsize=8, halign='left')
d_top += elm.Label().at((9, 1.9)).label('R6: 330Ω 1/4W (×3)', fontsize=8, halign='left')

d_top += elm.Label().at((9, 1.3)).label('Semiconductors:', fontsize=9, halign='left', font='bold')
d_top += elm.Label().at((9, 0.9)).label('D1,D2: BAT85 DO-35', fontsize=8, halign='left')
d_top += elm.Label().at((9, 0.5)).label('LED1: White 3mm', fontsize=8, halign='left')
d_top += elm.Label().at((9, 0.1)).label('LED2: RGB 5mm CC', fontsize=8, halign='left')

d_top += elm.Label().at((9, -0.5)).label('Capacitors:', fontsize=9, halign='left', font='bold')
d_top += elm.Label().at((9, -0.9)).label('C11,C13: 10µF elec', fontsize=8, halign='left')
d_top += elm.Label().at((9, -1.3)).label('C12,C14: 0.1µF cer', fontsize=8, halign='left')
d_top += elm.Label().at((9, -1.7)).label('C15,C16: 100nF (opt)', fontsize=8, halign='left')

# Notes
d_top += elm.Label().at((0, -3)).label('NOTES:', fontsize=11, halign='left', font='bold')
d_top += elm.Label().at((0, -3.5)).label('1. BAT85 cathode (banded end) connects to 3.3V rail', fontsize=8, halign='left')
d_top += elm.Label().at((0, -3.9)).label('2. Voltage dividers scale 5V input to 2.5V (safe for ADC)', fontsize=8, halign='left')
d_top += elm.Label().at((0, -4.3)).label('3. BAT85 clamps spikes to 3.7V max (within M4 3.8V abs max)', fontsize=8, halign='left')
d_top += elm.Label().at((0, -4.7)).label('4. RGB LED is common cathode (all cathodes to GND)', fontsize=8, halign='left')
d_top += elm.Label().at((0, -5.1)).label('5. Protection: SAFE for 0-40V+ input with BAT85 installed', fontsize=8, halign='left')

d_top.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_BOARD_COMPLETE.svg')
print("✅ TOP_BOARD_COMPLETE.svg saved")

# ============================================================================
# BOTTOM BOARD COMPLETE - All Output Circuits
# ============================================================================

d_bot = schemdraw.Drawing()

# Title
d_bot += elm.Label().at((0, 20)).label('PRISME BOTTOM BOARD - COMPLETE SCHEMATIC', fontsize=16, halign='left', font='bold')
d_bot += elm.Label().at((0, 19.2)).label('Output Board: MCP4728 DAC, CV/TRIG/CC outputs, S-Trig, Power', fontsize=11, halign='left')
d_bot += elm.Label().at((0, 18.6)).label('PCB Size: 90mm × 55mm | Date: 2025-11-03', fontsize=9, halign='left')

# ============================================================================
# SECTION 1: POWER RAILS (BOTTOM BOARD)
# ============================================================================

d_bot += elm.Label().at((0, 17.5)).label('POWER DISTRIBUTION', fontsize=13, halign='left', font='bold')

# USB-C Input
d_bot += elm.Label().at((0, 16.5)).label('USB-C Power Input:', fontsize=10, halign='left', font='bold')
usb_in = (2, 16)
d_bot += elm.Dot().at(usb_in).label('USB-C\n5V IN', fontsize=9, halign='right')
d_bot += elm.Line().right(1)
d_bot += elm.Dot().label('To M4 USB', fontsize=8, halign='left')

# 5V Rail
d_bot += elm.Label().at((0, 14.5)).label('5V Rail (powers DAC):', fontsize=10, halign='left', font='bold')
pwr_5v = (2, 14)
d_bot += elm.Dot().at(pwr_5v).label('From M4\nUSB Pin', fontsize=9, halign='right')
d_bot += elm.Line().right(1)
d_bot += elm.Vdd().label('5V', fontsize=9)

# 5V decoupling
d_bot += elm.Line().at((pwr_5v[0] + 1, pwr_5v[1])).down(0.5)
d_bot += elm.Capacitor().down(1.2).label('C1\n47µF', fontsize=8, loc='right')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

d_bot += elm.Line().at((pwr_5v[0] + 1, pwr_5v[1] - 0.5)).right(1.5)
d_bot += elm.Capacitor().down(1.2).label('C2\n0.1µF', fontsize=8, loc='right')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

# 5V to DAC
d_bot += elm.Line().at((pwr_5v[0] + 1, pwr_5v[1])).right(3)
d_bot += elm.Dot().label('To DAC\nVDD', fontsize=8, halign='left')

# 3.3V Rail
d_bot += elm.Label().at((7, 14.5)).label('3.3V Rail (MIDI/OLED/LEDs):', fontsize=10, halign='left', font='bold')
pwr_3v3 = (10, 14)
d_bot += elm.Dot().at(pwr_3v3).label('From M4\n3V3 Pin', fontsize=9, halign='right')
d_bot += elm.Line().right(1)
d_bot += elm.Vdd().label('3.3V', fontsize=9)

# 3.3V decoupling
d_bot += elm.Line().at((pwr_3v3[0] + 1, pwr_3v3[1])).down(0.5)
d_bot += elm.Capacitor().down(1.2).label('C9\n10µF', fontsize=8, loc='right')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

d_bot += elm.Line().at((pwr_3v3[0] + 1, pwr_3v3[1] - 0.5)).right(1.5)
d_bot += elm.Capacitor().down(1.2).label('C10\n0.1µF', fontsize=8, loc='right')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

# ============================================================================
# SECTION 2: MCP4728 DAC
# ============================================================================

d_bot += elm.Label().at((0, 11.5)).label('MCP4728 I2C DAC (0x60)', fontsize=13, halign='left', font='bold')

# I2C connections
d_bot += elm.Label().at((0, 10.5)).label('I2C Bus:', fontsize=10, halign='left', font='bold')
i2c_sda = (1, 10)
d_bot += elm.Dot().at(i2c_sda).label('From M4\nSDA', fontsize=8, halign='right')
d_bot += elm.Line().right(2)
d_bot += elm.Dot().label('DAC SDA', fontsize=8, halign='left')

i2c_scl = (1, 9.2)
d_bot += elm.Dot().at(i2c_scl).label('From M4\nSCL', fontsize=8, halign='right')
d_bot += elm.Line().right(2)
d_bot += elm.Dot().label('DAC SCL', fontsize=8, halign='left')

d_bot += elm.Label().at((0, 8.4)).label('Note: SDA/SCL shared with OLED Wing', fontsize=8, halign='left')

# ============================================================================
# SECTION 3: DAC OUTPUTS
# ============================================================================

d_bot += elm.Label().at((0, 7.5)).label('DAC OUTPUTS (0-5V, 1V/octave)', fontsize=13, halign='left', font='bold')

# Channel A - CV OUT
d_bot += elm.Label().at((0, 6.5)).label('CH A - CV OUT:', fontsize=10, halign='left', font='bold')
cv_out = (2, 6)
d_bot += elm.Dot().at(cv_out).label('DAC VA', fontsize=8, halign='right')
d_bot += elm.Line().right(0.8)
d_bot += elm.Resistor().right(2).label('R1 100Ω', fontsize=8, loc='top')
d_bot += elm.Line().right(0.5)
d_bot += elm.Dot().label('CV OUT\nJack TIP', fontsize=8, halign='left')
d_bot += elm.Line().at((cv_out[0] + 3.3, cv_out[1])).down(0.8)
d_bot += elm.Dot().label('Jack SLEEVE', fontsize=7, halign='left')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

# Channel B - TRIG OUT (V-Trig)
d_bot += elm.Label().at((0, 4)).label('CH B - TRIG OUT (V-Trig):', fontsize=10, halign='left', font='bold')
trig_out = (2, 3.5)
d_bot += elm.Dot().at(trig_out).label('DAC VB', fontsize=8, halign='right')
d_bot += elm.Line().right(0.8)
d_bot += elm.Resistor().right(2).label('R2 100Ω', fontsize=8, loc='top')
d_bot += elm.Line().right(0.5)
d_bot += elm.Dot().label('TRIG OUT\nJack TIP', fontsize=8, halign='left')
d_bot += elm.Line().at((trig_out[0] + 3.3, trig_out[1])).down(0.8)
d_bot += elm.Dot().label('Jack SLEEVE', fontsize=7, halign='left')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

# Channel C - CC OUT
d_bot += elm.Label().at((0, 1.5)).label('CH C - CC OUT:', fontsize=10, halign='left', font='bold')
cc_out = (2, 1)
d_bot += elm.Dot().at(cc_out).label('DAC VC', fontsize=8, halign='right')
d_bot += elm.Line().right(0.8)
d_bot += elm.Resistor().right(2).label('R3 100Ω', fontsize=8, loc='top')
d_bot += elm.Line().right(0.5)
d_bot += elm.Dot().label('CC OUT\nJack TIP', fontsize=8, halign='left')
d_bot += elm.Line().at((cc_out[0] + 3.3, cc_out[1])).down(0.8)
d_bot += elm.Dot().label('Jack SLEEVE', fontsize=7, halign='left')
d_bot += elm.Line().down(0.3)
d_bot += elm.Ground()

# ============================================================================
# SECTION 4: S-TRIG CIRCUIT
# ============================================================================

d_bot += elm.Label().at((0, -1)).label('S-TRIG CIRCUIT (Alternate TRIG OUT mode)', fontsize=13, halign='left', font='bold')

# GPIO input
gpio_d10 = (1, -2.5)
d_bot += elm.Dot().at(gpio_d10).label('From M4\nD10 GPIO', fontsize=8, halign='right')

# Base resistor
d_bot += elm.Line().right(0.8)
d_bot += elm.Resistor().right(2).label('R8 1kΩ', fontsize=8, loc='top')

# NPN transistor
q_pos = (gpio_d10[0] + 2.8, gpio_d10[1])
d_bot += elm.Bjt(circle=True).at(q_pos).label('Q1\n2N3904', fontsize=8, loc='bottom')

# Collector to jack
d_bot += elm.Line().at((q_pos[0], q_pos[1] + 0.8)).up(0.5)
d_bot += elm.Resistor().up(1.2).label('R9 100Ω', fontsize=8, loc='right')
d_bot += elm.Line().up(0.5)
d_bot += elm.Dot().label('TRIG OUT\nJack TIP\n(S-Trig)', fontsize=8, halign='left')

# Emitter to ground
d_bot += elm.Line().at((q_pos[0], q_pos[1] - 0.8)).down(0.5)
d_bot += elm.Ground()

d_bot += elm.Label().at((7, -2)).label('Operation:', fontsize=9, halign='left', font='bold')
d_bot += elm.Label().at((7, -2.5)).label('D10 LOW: Jack OPEN', fontsize=8, halign='left')
d_bot += elm.Label().at((7, -2.9)).label('D10 HIGH: Jack to GND', fontsize=8, halign='left')
d_bot += elm.Label().at((7, -3.3)).label('(Vintage synth trig)', fontsize=8, halign='left')

# ============================================================================
# SECTION 5: M4 CONNECTIONS SUMMARY
# ============================================================================

d_bot += elm.Label().at((9, 11.5)).label('M4 CONNECTIONS', fontsize=12, halign='left', font='bold')
d_bot += elm.Label().at((9, 11)).label('Power:', fontsize=10, halign='left', font='bold')
d_bot += elm.Label().at((9, 10.6)).label('• USB → 5V Rail → DAC', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 10.2)).label('• 3V3 → 3.3V Rail', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 9.8)).label('• GND → Common GND', fontsize=8, halign='left')

d_bot += elm.Label().at((9, 9.2)).label('I2C Bus:', fontsize=10, halign='left', font='bold')
d_bot += elm.Label().at((9, 8.8)).label('• SDA → DAC SDA', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 8.4)).label('• SCL → DAC SCL', fontsize=8, halign='left')

d_bot += elm.Label().at((9, 7.8)).label('GPIO:', fontsize=10, halign='left', font='bold')
d_bot += elm.Label().at((9, 7.4)).label('• D10 → S-Trig base', fontsize=8, halign='left')

# ============================================================================
# SECTION 6: COMPONENT VALUES
# ============================================================================

d_bot += elm.Label().at((9, 6)).label('COMPONENT VALUES', fontsize=11, halign='left', font='bold')
d_bot += elm.Label().at((9, 5.6)).label('IC:', fontsize=9, halign='left', font='bold')
d_bot += elm.Label().at((9, 5.2)).label('MCP4728: Adafruit 4470', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 4.8)).label('I2C Addr: 0x60', fontsize=8, halign='left')

d_bot += elm.Label().at((9, 4.2)).label('Resistors:', fontsize=9, halign='left', font='bold')
d_bot += elm.Label().at((9, 3.8)).label('R1,R2,R3,R9: 100Ω 1/4W', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 3.4)).label('R8: 1kΩ 1/4W', fontsize=8, halign='left')

d_bot += elm.Label().at((9, 2.8)).label('Transistor:', fontsize=9, halign='left', font='bold')
d_bot += elm.Label().at((9, 2.4)).label('Q1: 2N3904 NPN TO-92', fontsize=8, halign='left')

d_bot += elm.Label().at((9, 1.8)).label('Capacitors:', fontsize=9, halign='left', font='bold')
d_bot += elm.Label().at((9, 1.4)).label('C1: 47µF electrolytic', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 1)).label('C2: 0.1µF ceramic', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 0.6)).label('C9: 10µF electrolytic', fontsize=8, halign='left')
d_bot += elm.Label().at((9, 0.2)).label('C10: 0.1µF ceramic', fontsize=8, halign='left')

# Notes
d_bot += elm.Label().at((0, -5)).label('NOTES:', fontsize=11, halign='left', font='bold')
d_bot += elm.Label().at((0, -5.5)).label('1. MCP4728 MUST be powered by 5V for 0-5V output range', fontsize=8, halign='left')
d_bot += elm.Label().at((0, -5.9)).label('2. All DAC outputs have 100Ω series protection (short-circuit safe)', fontsize=8, halign='left')
d_bot += elm.Label().at((0, -6.3)).label('3. V-Trig (DAC) and S-Trig (transistor) share same jack (select mode in software)', fontsize=8, halign='left')
d_bot += elm.Label().at((0, -6.7)).label('4. I2C bus shared with OLED Wing (0x3C) - both on same SDA/SCL wires', fontsize=8, halign='left')
d_bot += elm.Label().at((0, -7.1)).label('5. Output specs: 0-5V (5 octaves), 1V/octave Eurorack, 12-bit resolution', fontsize=8, halign='left')

d_bot.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_BOARD_COMPLETE.svg')
print("✅ BOTTOM_BOARD_COMPLETE.svg saved")

print("\n✅ COMPLETE BOARD SCHEMATICS READY:")
print("   TOP_BOARD_COMPLETE.svg - All input circuits + power")
print("   BOTTOM_BOARD_COMPLETE.svg - All output circuits + DAC + S-Trig + power")
