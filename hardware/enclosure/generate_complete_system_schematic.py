#!/usr/bin/env python3
"""
Generate COMPLETE SYSTEM SCHEMATIC - All Components
Session 25 - Shows M4, MIDI Wing, OLED Wing, and both custom PCBs
"""

import schemdraw
import schemdraw.elements as elm

# Create new drawing with larger canvas
d = schemdraw.Drawing()

# Title block
d += elm.Label().at((0, 16)).label('PRISME COMPLETE SYSTEM SCHEMATIC', fontsize=16, halign='left', font='bold')
d += elm.Label().at((0, 15.3)).label('Shows ALL components: M4, MIDI Wing, OLED Wing, Input PCB, Output PCB', fontsize=10, halign='left')
d += elm.Label().at((0, 14.8)).label('Date: 2025-11-03 (Session 25)', fontsize=8, halign='left')

# ============================================================================
# SECTION 1: FEATHER M4 CAN EXPRESS (Center of system)
# ============================================================================

d += elm.Label().at((6, 14)).label('FEATHER M4 CAN EXPRESS', fontsize=14, halign='center', font='bold')

# Draw M4 as IC with key pins
m4_center = (6, 11)
d += elm.Ic(pins=[
    # Left side - Power
    elm.IcPin(name='USB 5V', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='3V3', side='left', pin='3'),
    # Left side - I2C
    elm.IcPin(name='SDA', side='left', pin='4'),
    elm.IcPin(name='SCL', side='left', pin='5'),
    # Left side - UART
    elm.IcPin(name='RX', side='left', pin='6'),
    elm.IcPin(name='TX', side='left', pin='7'),
    # Right side - ADC inputs
    elm.IcPin(name='A3', side='right', pin='8'),
    elm.IcPin(name='A4', side='right', pin='9'),
    # Right side - GPIO outputs
    elm.IcPin(name='D4', side='right', pin='10'),
    elm.IcPin(name='D10', side='right', pin='11'),
    elm.IcPin(name='D11', side='right', pin='12'),
    elm.IcPin(name='D23', side='right', pin='13'),
    elm.IcPin(name='D24', side='right', pin='14'),
]).at(m4_center).label('Adafruit\nFeather M4\nCAN Express', fontsize=10, loc='center')

# ============================================================================
# SECTION 2: POWER DISTRIBUTION
# ============================================================================

d += elm.Label().at((0, 8)).label('POWER RAILS', fontsize=12, halign='left', font='bold')

# USB 5V input
usb_pos = (m4_center[0] - 3, m4_center[1] + 3)
d += elm.Line().at(usb_pos).left(1)
d += elm.Dot().label('USB-C\n5V IN', fontsize=8, halign='right')

# 5V rail from M4
d += elm.Line().at(usb_pos).down(1)
five_v_rail = (usb_pos[0], usb_pos[1] - 1)
d += elm.Vdd().at(five_v_rail).label('5V Rail', fontsize=9)

# 5V to DAC (on output board)
d += elm.Line().at(five_v_rail).right(6)
d += elm.Dot().label('To DAC\n(Output PCB)', fontsize=7, halign='left')

# 3.3V rail from M4
three_v_rail = (m4_center[0] - 3, m4_center[1] + 1)
d += elm.Line().at(three_v_rail).down(1)
d += elm.Vdd().at((three_v_rail[0], three_v_rail[1] - 1)).label('3.3V Rail', fontsize=9)

# 3.3V to peripherals
three_v_dist = (three_v_rail[0], three_v_rail[1] - 1)
d += elm.Line().at(three_v_dist).right(6)
d += elm.Dot().label('To MIDI Wing\nOLED Wing\nLEDs', fontsize=7, halign='left')

# Ground
gnd_pos = (m4_center[0] - 3, m4_center[1] + 2)
d += elm.Line().at(gnd_pos).down(0.5)
d += elm.Ground().label('Common GND', fontsize=8)

# ============================================================================
# SECTION 3: OLED FEATHERWING (I2C)
# ============================================================================

d += elm.Label().at((0, 5)).label('OLED DISPLAY', fontsize=12, halign='left', font='bold')

oled_pos = (2, 3)
d += elm.Ic(pins=[
    elm.IcPin(name='3V3', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='SDA', side='right', pin='3'),
    elm.IcPin(name='SCL', side='right', pin='4'),
]).at(oled_pos).label('OLED Wing\n128x64\n0x3C', fontsize=9, loc='center')

# Power connections
d += elm.Line().at((oled_pos[0] - 1, oled_pos[1] + 1)).left(0.5)
d += elm.Vdd().label('3.3V', fontsize=7)
d += elm.Line().at((oled_pos[0] - 1, oled_pos[1] + 0.3)).left(0.3)
d += elm.Ground()

# I2C connections to M4
i2c_sda_oled = (oled_pos[0] + 1, oled_pos[1] + 0.3)
d += elm.Line().at(i2c_sda_oled).right(2.5)
d += elm.Dot().label('M4 SDA', fontsize=7, halign='left')

i2c_scl_oled = (oled_pos[0] + 1, oled_pos[1] - 0.4)
d += elm.Line().at(i2c_scl_oled).right(2.5)
d += elm.Dot().label('M4 SCL', fontsize=7, halign='left')

# ============================================================================
# SECTION 4: MIDI FEATHERWING (UART)
# ============================================================================

d += elm.Label().at((0, 1)).label('MIDI I/O', fontsize=12, halign='left', font='bold')

midi_pos = (2, -1)
d += elm.Ic(pins=[
    elm.IcPin(name='3V3', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='RX', side='right', pin='3'),
    elm.IcPin(name='TX', side='right', pin='4'),
]).at(midi_pos).label('MIDI Wing\nDIN-5 I/O', fontsize=9, loc='center')

# Power connections
d += elm.Line().at((midi_pos[0] - 1, midi_pos[1] + 1)).left(0.5)
d += elm.Vdd().label('3.3V', fontsize=7)
d += elm.Line().at((midi_pos[0] - 1, midi_pos[1] + 0.3)).left(0.3)
d += elm.Ground()

# UART connections to M4
uart_rx = (midi_pos[0] + 1, midi_pos[1] + 0.3)
d += elm.Line().at(uart_rx).right(2.5)
d += elm.Dot().label('M4 RX', fontsize=7, halign='left')

uart_tx = (midi_pos[0] + 1, midi_pos[1] - 0.4)
d += elm.Line().at(uart_tx).right(2.5)
d += elm.Dot().label('M4 TX', fontsize=7, halign='left')

# MIDI jacks
d += elm.Line().at((midi_pos[0] - 1, midi_pos[1] - 0.4)).left(1)
d += elm.Dot().label('MIDI IN\nDIN-5', fontsize=7, halign='right')
d += elm.Line().at((midi_pos[0] - 1, midi_pos[1] - 1)).left(1)
d += elm.Dot().label('MIDI OUT\nDIN-5', fontsize=7, halign='right')

# ============================================================================
# SECTION 5: INPUT PCB (TOP BOARD)
# ============================================================================

d += elm.Label().at((10, 5)).label('INPUT PCB (TOP BOARD)', fontsize=12, halign='left', font='bold')

# CV IN circuit
d += elm.Label().at((10, 4)).label('CV IN Circuit:', fontsize=10, halign='left')
cv_in_jack = (10, 3.5)
d += elm.Dot().at(cv_in_jack).label('CV IN\nJack', fontsize=7, halign='right')

# Voltage divider
d += elm.Line().at(cv_in_jack).right(0.5)
d += elm.Resistor().right(1).label('10kΩ', fontsize=7, loc='top')
cv_tap = (cv_in_jack[0] + 1.5, cv_in_jack[1])
d += elm.Dot().at(cv_tap)

# To M4 A3
d += elm.Line().at(cv_tap).right(1.5)
d += elm.Dot().label('To M4 A3', fontsize=7, halign='left')

# Lower resistor to ground
d += elm.Line().at(cv_tap).down(0.5)
d += elm.Resistor().down(0.7).label('10kΩ', fontsize=7, loc='right')
d += elm.Line().down(0.2)
d += elm.Ground()

# BAT85 clamp
d += elm.Line().at(cv_tap).up(0.5)
d += elm.Diode().up(0.7).label('BAT85', fontsize=7, loc='left')
d += elm.Line().up(0.2)
d += elm.Vdd().label('3.3V', fontsize=7)

# TRIG IN circuit
d += elm.Label().at((10, 1.5)).label('TRIG IN Circuit:', fontsize=10, halign='left')
trig_in_jack = (10, 1)
d += elm.Dot().at(trig_in_jack).label('TRIG IN\nJack', fontsize=7, halign='right')

# Voltage divider
d += elm.Line().at(trig_in_jack).right(0.5)
d += elm.Resistor().right(1).label('10kΩ', fontsize=7, loc='top')
trig_tap = (trig_in_jack[0] + 1.5, trig_in_jack[1])
d += elm.Dot().at(trig_tap)

# To M4 A4
d += elm.Line().at(trig_tap).right(1.5)
d += elm.Dot().label('To M4 A4', fontsize=7, halign='left')

# Lower resistor to ground
d += elm.Line().at(trig_tap).down(0.5)
d += elm.Resistor().down(0.7).label('10kΩ', fontsize=7, loc='right')
d += elm.Line().down(0.2)
d += elm.Ground()

# BAT85 clamp
d += elm.Line().at(trig_tap).up(0.5)
d += elm.Diode().up(0.7).label('BAT85', fontsize=7, loc='left')
d += elm.Line().up(0.2)
d += elm.Vdd().label('3.3V', fontsize=7)

# ============================================================================
# SECTION 6: OUTPUT PCB (BOTTOM BOARD)
# ============================================================================

d += elm.Label().at((10, -1)).label('OUTPUT PCB (BOTTOM BOARD)', fontsize=12, halign='left', font='bold')

# MCP4728 DAC
dac_pos = (11, -3)
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='SDA', side='left', pin='3'),
    elm.IcPin(name='SCL', side='left', pin='4'),
    elm.IcPin(name='VA', side='right', pin='5'),
    elm.IcPin(name='VB', side='right', pin='6'),
    elm.IcPin(name='VC', side='right', pin='7'),
]).at(dac_pos).label('MCP4728\nI2C DAC\n0x60', fontsize=9, loc='center')

# Power connections
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] + 1.5)).left(0.5)
d += elm.Vdd().label('5V', fontsize=7)
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] + 0.8)).left(0.3)
d += elm.Ground()

# I2C connections
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] + 0.1)).left(2)
d += elm.Dot().label('M4 SDA', fontsize=7, halign='right')
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] - 0.6)).left(2)
d += elm.Dot().label('M4 SCL', fontsize=7, halign='right')

# CV OUT (Channel A)
va_out = (dac_pos[0] + 1, dac_pos[1] + 1.5)
d += elm.Line().at(va_out).right(0.5)
d += elm.Resistor().right(1).label('100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CV OUT\nJack', fontsize=7, halign='left')

# TRIG OUT V-Trig (Channel B)
vb_out = (dac_pos[0] + 1, dac_pos[1] + 0.8)
d += elm.Line().at(vb_out).right(0.5)
d += elm.Resistor().right(1).label('100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('TRIG OUT\n(V-Trig)\nJack', fontsize=7, halign='left')

# CC OUT (Channel C)
vc_out = (dac_pos[0] + 1, dac_pos[1] + 0.1)
d += elm.Line().at(vc_out).right(0.5)
d += elm.Resistor().right(1).label('100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CC OUT\nJack', fontsize=7, halign='left')

# S-Trig circuit (alternate TRIG OUT mode)
d += elm.Label().at((10, -6)).label('S-Trig Circuit (alternate mode):', fontsize=10, halign='left')
strig_gpio = (10, -7)
d += elm.Dot().at(strig_gpio).label('M4 D10', fontsize=7, halign='right')
d += elm.Line().at(strig_gpio).right(0.5)
d += elm.Resistor().right(1).label('1kΩ', fontsize=7, loc='top')

# NPN transistor
transistor_pos = (strig_gpio[0] + 1.5, strig_gpio[1])
d += elm.Bjt(circle=True).at(transistor_pos).label('2N3904', fontsize=7, loc='bottom')

# Collector to TRIG OUT jack
d += elm.Line().at((transistor_pos[0], transistor_pos[1] + 0.7)).up(0.3)
d += elm.Resistor().up(0.7).label('100Ω', fontsize=7, loc='right')
d += elm.Line().up(0.3)
d += elm.Dot().label('TRIG OUT\n(S-Trig)', fontsize=7, halign='left')

# Emitter to ground
d += elm.Line().at((transistor_pos[0], transistor_pos[1] - 0.7)).down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 7: LED INDICATORS
# ============================================================================

d += elm.Label().at((10, -9)).label('LED INDICATORS (from M4 GPIOs):', fontsize=10, halign='left')
d += elm.Label().at((10, -9.5)).label('D4 → CV IN LED (white, 1kΩ)', fontsize=8, halign='left')
d += elm.Label().at((10, -10)).label('D11 → TRIG IN LED R (RGB, 330Ω)', fontsize=8, halign='left')
d += elm.Label().at((10, -10.5)).label('D23 → TRIG IN LED G (RGB, 330Ω)', fontsize=8, halign='left')
d += elm.Label().at((10, -10.8)).label('D24 → TRIG IN LED B (RGB, 330Ω)', fontsize=8, halign='left')

# ============================================================================
# SECTION 8: CONNECTION SUMMARY
# ============================================================================

d += elm.Label().at((0, -3)).label('PIN CONNECTIONS SUMMARY:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((0, -3.7)).label('M4 Power:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -4.2)).label('  USB 5V → 5V Rail → MCP4728 VDD', fontsize=8, halign='left')
d += elm.Label().at((0, -4.7)).label('  3V3 → 3.3V Rail → MIDI Wing, OLED Wing, LEDs, BAT85 clamps', fontsize=8, halign='left')
d += elm.Label().at((0, -5.2)).label('  GND → Common Ground', fontsize=8, halign='left')

d += elm.Label().at((0, -6)).label('M4 I2C (shared bus):', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -6.5)).label('  SDA → OLED Wing (0x3C), MCP4728 DAC (0x60)', fontsize=8, halign='left')
d += elm.Label().at((0, -6.8)).label('  SCL → OLED Wing (0x3C), MCP4728 DAC (0x60)', fontsize=8, halign='left')

d += elm.Label().at((0, -7.5)).label('M4 UART (Serial1):', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -8)).label('  RX ← MIDI Wing (MIDI IN)', fontsize=8, halign='left')
d += elm.Label().at((0, -8.5)).label('  TX → MIDI Wing (MIDI OUT)', fontsize=8, halign='left')

d += elm.Label().at((0, -9.2)).label('M4 ADC Inputs (Input PCB):', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -9.7)).label('  A3 ← CV IN (via 10kΩ/10kΩ divider + BAT85)', fontsize=8, halign='left')
d += elm.Label().at((0, -10.2)).label('  A4 ← TRIG IN (via 10kΩ/10kΩ divider + BAT85)', fontsize=8, halign='left')

d += elm.Label().at((0, -10.9)).label('M4 GPIO Outputs:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -11.4)).label('  D4 → CV IN LED (white)', fontsize=8, halign='left')
d += elm.Label().at((0, -11.9)).label('  D10 → S-Trig transistor base (via 1kΩ)', fontsize=8, halign='left')
d += elm.Label().at((0, -12.4)).label('  D11, D23, D24 → RGB LED channels', fontsize=8, halign='left')

# ============================================================================
# SECTION 9: PCB DESIGN NOTES
# ============================================================================

d += elm.Label().at((0, -13.5)).label('PCB DESIGN NOTES:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((0, -14)).label('1. Input PCB contains: Voltage dividers, BAT85 clamps, input jacks, input LEDs', fontsize=8, halign='left')
d += elm.Label().at((0, -14.5)).label('2. Output PCB contains: MCP4728 DAC, output jacks, S-Trig circuit, output LEDs', fontsize=8, halign='left')
d += elm.Label().at((0, -15)).label('3. M4/MIDI/OLED Wings are PRE-BUILT - connect via headers/wires', fontsize=8, halign='left')
d += elm.Label().at((0, -15.5)).label('4. Both PCBs need: 5V and 3.3V power rails with decoupling (C1/C2 + C9/C10 per board)', fontsize=8, halign='left')
d += elm.Label().at((0, -16)).label('5. I2C bus shared between OLED (0x3C) and DAC (0x60) - use common SDA/SCL traces', fontsize=8, halign='left')

# Save schematic
d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/COMPLETE_SYSTEM_SCHEMATIC.svg')
print("COMPLETE SYSTEM SCHEMATIC saved to: COMPLETE_SYSTEM_SCHEMATIC.svg")
print("File size:", len(open('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/COMPLETE_SYSTEM_SCHEMATIC.svg').read()), "bytes")
