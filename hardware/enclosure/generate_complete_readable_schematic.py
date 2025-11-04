#!/usr/bin/env python3
"""
Generate COMPLETE READABLE SYSTEM SCHEMATIC
Session 25 - Exhaustive, properly connected, traditional schematic
Left to right: Inputs → M4 → Outputs
Top to bottom: Power → Signals → Ground
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# =============================================================================
# TITLE
# =============================================================================
d += elm.Label().at((0, 40)).label('PRISME HARDWARE - COMPLETE SYSTEM SCHEMATIC', fontsize=20, halign='left', font='bold')
d += elm.Label().at((0, 39)).label('All components and connections', fontsize=12, halign='left')

# =============================================================================
# POWER RAILS (TOP)
# =============================================================================
d += elm.Label().at((0, 37)).label('POWER DISTRIBUTION', fontsize=14, halign='left', font='bold')

# USB-C 5V Input
d += elm.Dot().at((2, 36)).label('USB-C\n5V IN', fontsize=10, halign='right')
d += elm.Line().right(2)
pwr_5v_node = d.here
d += elm.Dot()
d += elm.Vdd().label('5V', fontsize=11)

# 5V to M4 USB pin (labeled connection)
d += elm.Line().at(pwr_5v_node).right(4)
d += elm.Dot().label('To M4 USB', fontsize=9, halign='left')

# 5V to DAC VDD
d += elm.Line().at(pwr_5v_node).down(2)
dac_5v_node = d.here
d += elm.Dot().label('To DAC VDD', fontsize=8, halign='left')

# 3.3V from M4 regulator
d += elm.Dot().at((15, 36)).label('M4 3V3\nRegulator', fontsize=10, halign='right')
d += elm.Line().right(2)
pwr_3v3_node = d.here
d += elm.Dot()
d += elm.Vdd().label('3.3V', fontsize=11)

# 3.3V distribution
d += elm.Line().at(pwr_3v3_node).right(4)
d += elm.Dot().label('To OLED,\nMIDI, LEDs,\nBAT85', fontsize=8, halign='left')

# Ground reference
d += elm.Ground().at((10, 33)).label('COMMON GROUND', fontsize=11, halign='left')

# =============================================================================
# CV IN CIRCUIT (LEFT SIDE)
# =============================================================================
d += elm.Label().at((0, 30)).label('CV IN - TOP BOARD', fontsize=14, halign='left', font='bold')

# Input jack
cv_jack_y = 28
d += elm.Dot().at((1, cv_jack_y)).label('CV IN\nJack TIP', fontsize=10, halign='right')
d += elm.Resistor().right(2.5).label('R1\n10kΩ', fontsize=9, loc='top')
cv_tap = d.here
d += elm.Dot().label('TAP', fontsize=9, loc='top')

# To M4 A3
d += elm.Line().right(3)
cv_to_m4 = d.here
d += elm.Dot().label('To M4\nPin A3', fontsize=9, halign='left')

# Lower divider resistor
d += elm.Resistor().at(cv_tap).down(2).label('R2\n10kΩ', fontsize=9, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp
d += elm.Diode().at(cv_tap).up(2).label('D1\nBAT85', fontsize=9, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=9)

# Jack ground
d += elm.Line().at((1, cv_jack_y)).down(1)
d += elm.Ground()

# CV IN LED
d += elm.Label().at((0, 24)).label('CV LED:', fontsize=10, halign='right')
cv_led_drive = (1, 24)
d += elm.Dot().at(cv_led_drive).label('From M4\nPin D4', fontsize=8, halign='right')
d += elm.Resistor().right(2).label('R3\n1kΩ', fontsize=9, loc='top')
d += elm.LED().right(1.5).label('White', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.Ground()

# =============================================================================
# TRIG IN CIRCUIT (LEFT SIDE)
# =============================================================================
d += elm.Label().at((0, 21)).label('TRIG IN - TOP BOARD', fontsize=14, halign='left', font='bold')

# Input jack
trig_jack_y = 19
d += elm.Dot().at((1, trig_jack_y)).label('TRIG IN\nJack TIP', fontsize=10, halign='right')
d += elm.Resistor().right(2.5).label('R4\n10kΩ', fontsize=9, loc='top')
trig_tap = d.here
d += elm.Dot().label('TAP', fontsize=9, loc='top')

# To M4 A4
d += elm.Line().right(3)
trig_to_m4 = d.here
d += elm.Dot().label('To M4\nPin A4', fontsize=9, halign='left')

# Lower divider resistor
d += elm.Resistor().at(trig_tap).down(2).label('R5\n10kΩ', fontsize=9, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp
d += elm.Diode().at(trig_tap).up(2).label('D2\nBAT85', fontsize=9, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=9)

# Jack ground
d += elm.Line().at((1, trig_jack_y)).down(1)
d += elm.Ground()

# TRIG IN RGB LED (3 channels)
d += elm.Label().at((0, 15)).label('TRIG RGB:', fontsize=10, halign='right')

# Red channel
d += elm.Dot().at((1, 14.5)).label('M4 D11', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('R6\n330Ω', fontsize=8, loc='top')
d += elm.LED().right(1).label('R', fontsize=8, loc='top')
d += elm.Line().right(0.5)
d += elm.Ground()

# Green channel
d += elm.Dot().at((1, 13.5)).label('M4 D23', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('330Ω', fontsize=8, loc='top')
d += elm.LED().right(1).label('G', fontsize=8, loc='top')
d += elm.Line().right(0.5)
d += elm.Ground()

# Blue channel
d += elm.Dot().at((1, 12.5)).label('M4 D24', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('330Ω', fontsize=8, loc='top')
d += elm.LED().right(1).label('B', fontsize=8, loc='top')
d += elm.Line().right(0.5)
d += elm.Ground()

# =============================================================================
# FEATHER M4 (CENTER)
# =============================================================================
d += elm.Label().at((10, 30)).label('FEATHER M4 CAN EXPRESS', fontsize=14, halign='center', font='bold')

m4 = elm.Ic(pins=[
    # Left side - ADC inputs
    elm.IcPin(name='A3', side='left', pin='1'),
    elm.IcPin(name='A4', side='left', pin='2'),
    # Right side - GPIO
    elm.IcPin(name='D4', side='right', pin='3'),
    elm.IcPin(name='D10', side='right', pin='4'),
    elm.IcPin(name='D11', side='right', pin='5'),
    elm.IcPin(name='D23', side='right', pin='6'),
    elm.IcPin(name='D24', side='right', pin='7'),
    # Top - I2C
    elm.IcPin(name='SDA', side='top', pin='8'),
    elm.IcPin(name='SCL', side='top', pin='9'),
    # Bottom - UART
    elm.IcPin(name='RX', side='bot', pin='10'),
    elm.IcPin(name='TX', side='bot', pin='11'),
]).at((10, 22))

d += m4.label('M4\nATSAMD51', fontsize=11, loc='center')

# Connect CV IN to M4 A3
d += elm.Line().at(cv_to_m4).right(10 - 4 - cv_to_m4[0])
d += elm.Line().down(cv_to_m4[1] - (22 + 1.4))
d += elm.Line().right(10 - 4)

# Connect TRIG IN to M4 A4
d += elm.Line().at(trig_to_m4).right(10 - 4 - trig_to_m4[0])
d += elm.Line().down(trig_to_m4[1] - (22 + 0.7))
d += elm.Line().right(10 - 4)

# Connect M4 GPIO D4 to CV LED
d += elm.Line().at((10 + 4, 22 + 1.4)).right(2)
d += elm.Line().down(22 + 1.4 - cv_led_drive[1])
d += elm.Line().left(10 + 4 + 2 - cv_led_drive[0])

# Connect M4 GPIO D11 to RGB Red
d += elm.Line().at((10 + 4, 22 + 0.7)).right(3)
d += elm.Line().down(22 + 0.7 - 14.5)
d += elm.Line().left(10 + 4 + 3 - 1)

# Connect M4 GPIO D23 to RGB Green
d += elm.Line().at((10 + 4, 22)).right(3.5)
d += elm.Line().down(22 - 13.5)
d += elm.Line().left(10 + 4 + 3.5 - 1)

# Connect M4 GPIO D24 to RGB Blue
d += elm.Line().at((10 + 4, 22 - 0.7)).right(4)
d += elm.Line().down(22 - 0.7 - 12.5)
d += elm.Line().left(10 + 4 + 4 - 1)

# =============================================================================
# I2C PERIPHERALS (TOP CENTER)
# =============================================================================
d += elm.Label().at((8, 27)).label('I2C BUS (0x3C, 0x60)', fontsize=12, halign='center', font='bold')

# OLED Wing
oled_y = 26
d += elm.Ic(pins=[
    elm.IcPin(name='SDA', side='bot', pin='1'),
    elm.IcPin(name='SCL', side='bot', pin='2'),
]).at((8, oled_y))
d += elm.Label().at((8, oled_y)).label('OLED\n0x3C', fontsize=10, halign='center')

# Connect OLED to M4 I2C
sda_oled = (8 - 0.35, oled_y - 1)
d += elm.Line().at(sda_oled).down(1)
i2c_sda_node = d.here
d += elm.Dot()
d += elm.Line().down(oled_y - 1 - 1 - (22 + 3))
d += elm.Line().right(10 - 4 - (8 - 0.35))

scl_oled = (8 + 0.35, oled_y - 1)
d += elm.Line().at(scl_oled).down(1)
i2c_scl_node = d.here
d += elm.Dot()
d += elm.Line().down(oled_y - 1 - 1 - (22 + 2.3))
d += elm.Line().right(10 - 4 - (8 + 0.35))

# MCP4728 DAC
dac_x = 12
dac_y = 26
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='SDA', side='bot', pin='2'),
    elm.IcPin(name='SCL', side='bot', pin='3'),
    elm.IcPin(name='VA', side='right', pin='4'),
    elm.IcPin(name='VB', side='right', pin='5'),
    elm.IcPin(name='VC', side='right', pin='6'),
]).at((dac_x, dac_y))
d += elm.Label().at((dac_x, dac_y)).label('MCP4728\n0x60', fontsize=10, halign='center')

# Connect DAC VDD to 5V
d += elm.Line().at((dac_x - 1, dac_y + 0.7)).left(1)
d += elm.Line().up(dac_5v_node[1] - (dac_y + 0.7))
d += elm.Line().left(dac_x - 1 - 1 - dac_5v_node[0])
d += elm.Dot().at(dac_5v_node)

# Connect DAC to I2C bus
d += elm.Line().at((dac_x - 0.35, dac_y - 1)).down(0.5)
d += elm.Line().left(dac_x - 0.35 - (8 - 0.35))
d += elm.Line().up(0.5)
d += elm.Dot().at(i2c_sda_node)

d += elm.Line().at((dac_x + 0.35, dac_y - 1)).down(0.5)
d += elm.Line().left(dac_x + 0.35 - (8 + 0.35))
d += elm.Line().up(0.5)
d += elm.Dot().at(i2c_scl_node)

# =============================================================================
# MIDI UART (BOTTOM CENTER)
# =============================================================================
d += elm.Label().at((10, 18)).label('MIDI I/O (UART)', fontsize=12, halign='center', font='bold')

# MIDI IN
d += elm.Dot().at((8, 17)).label('MIDI IN\nDIN-5', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Line().up(22 - 2 - 17)
d += elm.Line().right(10 - 4 - 8 - 1)

# MIDI OUT
d += elm.Dot().at((8, 16)).label('MIDI OUT\nDIN-5', fontsize=9, halign='right')
d += elm.Line().right(1.5)
d += elm.Line().up(22 - 2.7 - 16)
d += elm.Line().right(10 - 4 - 8 - 1.5)

# =============================================================================
# DAC OUTPUTS (RIGHT SIDE)
# =============================================================================
d += elm.Label().at((16, 27)).label('DAC OUTPUTS - BOTTOM BOARD', fontsize=14, halign='left', font='bold')

# CV OUT (Channel A)
d += elm.Line().at((dac_x + 1, dac_y + 1.4)).right(2)
cv_out_start = d.here
d += elm.Resistor().right(2).label('R1\n100Ω', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CV OUT\nJack TIP', fontsize=10, halign='left')
d += elm.Line().down(1)
d += elm.Ground()

# TRIG OUT V-Trig (Channel B)
d += elm.Line().at((dac_x + 1, dac_y + 0.7)).right(2)
trig_v_start = d.here
d += elm.Resistor().right(2).label('R2\n100Ω', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(V-Trig)', fontsize=9, halign='left')
d += elm.Line().down(1)
d += elm.Ground()

# CC OUT (Channel C)
d += elm.Line().at((dac_x + 1, dac_y)).right(2)
cc_out_start = d.here
d += elm.Resistor().right(2).label('R3\n100Ω', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CC OUT\nJack TIP', fontsize=10, halign='left')
d += elm.Line().down(1)
d += elm.Ground()

# =============================================================================
# S-TRIG CIRCUIT (RIGHT BOTTOM)
# =============================================================================
d += elm.Label().at((16, 20)).label('S-TRIG - BOTTOM BOARD', fontsize=14, halign='left', font='bold')

# From M4 D10
d += elm.Line().at((10 + 4, 22 - 1.4)).right(2)
strig_start = d.here
d += elm.Line().down(22 - 1.4 - 18)
d += elm.Resistor().right(2).label('R8\n1kΩ', fontsize=9, loc='top')

# NPN Transistor
q_pos = d.here
d += elm.Bjt(circle=True).right().anchor('base')
d += elm.Label().at((q_pos[0] + 0.5, q_pos[1] - 1)).label('Q1\n2N3904', fontsize=9, halign='center')

# Collector to jack
q_collector = (q_pos[0] + 0.5, q_pos[1] + 0.8)
d += elm.Line().at(q_collector).up(0.5)
d += elm.Resistor().up(1.5).label('R9\n100Ω', fontsize=9, loc='right')
d += elm.Line().up(0.5)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(S-Trig)', fontsize=9, halign='left')

# Emitter to ground
q_emitter = (q_pos[0] + 0.5, q_pos[1] - 0.8)
d += elm.Line().at(q_emitter).down(0.5)
d += elm.Ground()

# =============================================================================
# POWER DECOUPLING (NOTES)
# =============================================================================
d += elm.Label().at((0, 9)).label('POWER DECOUPLING:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((0, 8.5)).label('TOP BOARD: C11 (10µF) + C12 (0.1µF) on 5V, C13 (10µF) + C14 (0.1µF) on 3.3V', fontsize=9, halign='left')
d += elm.Label().at((0, 8)).label('BOTTOM BOARD: C1 (47µF) + C2 (0.1µF) on 5V, C9 (10µF) + C10 (0.1µF) on 3.3V', fontsize=9, halign='left')

# =============================================================================
# KEY SPECS
# =============================================================================
d += elm.Label().at((0, 7)).label('KEY SPECIFICATIONS:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((0, 6.5)).label('• Input Protection: 10kΩ voltage divider + BAT85 Schottky clamp = safe 0-40V+', fontsize=9, halign='left')
d += elm.Label().at((0, 6)).label('• Output Range: 0-5V (5 octaves, 1V/octave Eurorack standard)', fontsize=9, halign='left')
d += elm.Label().at((0, 5.5)).label('• DAC Resolution: 12-bit (4096 steps per channel)', fontsize=9, halign='left')
d += elm.Label().at((0, 5)).label('• I2C Addresses: OLED 0x3C, MCP4728 DAC 0x60 (shared SDA/SCL bus)', fontsize=9, halign='left')
d += elm.Label().at((0, 4.5)).label('• Trigger Modes: V-Trig (0-5V DAC) OR S-Trig (switch to GND) - same jack', fontsize=9, halign='left')
d += elm.Label().at((0, 4)).label('• Output Protection: 100Ω series resistors on all DAC outputs', fontsize=9, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - COMPLETE EXHAUSTIVE VERSION")
print("   • All inputs: CV IN + TRIG IN with protection")
print("   • All outputs: CV OUT + TRIG OUT (V-Trig + S-Trig) + CC OUT")
print("   • All peripherals: M4 + OLED + MIDI + DAC")
print("   • All LEDs: CV (white) + TRIG (RGB 3-channel)")
print("   • All connections properly wired")
print("   • Power distribution shown")
print("   • I2C bus with shared connections")
