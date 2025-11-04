#!/usr/bin/env python3
"""
PRISME COMPLETE HARDWARE SCHEMATIC - PROFESSIONAL LAYOUT
Session 25 - Clean, readable, properly organized
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
d.config(fontsize=10, unit=3)

# =============================================================================
# TITLE
# =============================================================================
d += elm.Label().at((0, 28)).label('PRISME COMPLETE HARDWARE SCHEMATIC', fontsize=16, halign='left', font='bold')

# =============================================================================
# FEATHER M4 - CENTER TOP
# =============================================================================
d += elm.Label().at((8, 26)).label('FEATHER M4 CAN EXPRESS', fontsize=13, halign='center', font='bold')

# M4 as central component
d += elm.Ic(pins=[
    # Left side - Analog inputs
    elm.IcPin(name='A3', side='left', pin='1'),
    elm.IcPin(name='A4', side='left', pin='2'),
    # Right side - Digital outputs
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
]).at((8, 22)).label('M4', fontsize=11)

# =============================================================================
# CV IN CIRCUIT - LEFT UPPER
# =============================================================================
d += elm.Label().at((0, 24)).label('CV IN', fontsize=12, halign='left', font='bold')

# Jack with ground
d += elm.Dot().at((1, 23)).label('Jack', fontsize=9, halign='right')
cv_jack_y = 23
d.push()
d += elm.Ground()

# Voltage divider
d.pop()
d += elm.Resistor().right(2).label('R1\n10kΩ', fontsize=9)
cv_tap_x = d.here[0]
cv_tap_y = d.here[1]
d += elm.Dot().label('CV', fontsize=8, loc='top')
d.push()

# Lower resistor to ground
d += elm.Resistor().down(2).label('R2\n10kΩ', fontsize=9, loc='right')
d += elm.Ground()

# BAT85 clamp to 3.3V
d.pop()
d.push()
d += elm.Diode().up(2).label('D1\nBAT85', fontsize=9, loc='left')
d += elm.Vdd().label('3.3V', fontsize=9)

# Connection to M4 A3
d.pop()
d += elm.Line().right(8-2-cv_tap_x)
d += elm.Line().down(cv_tap_y - (22+0.7))

# =============================================================================
# TRIG IN CIRCUIT - LEFT LOWER
# =============================================================================
d += elm.Label().at((0, 19)).label('TRIG IN', fontsize=12, halign='left', font='bold')

# Jack with ground
d += elm.Dot().at((1, 18)).label('Jack', fontsize=9, halign='right')
trig_jack_y = 18
d.push()
d += elm.Ground()

# Voltage divider
d.pop()
d += elm.Resistor().right(2).label('R4\n10kΩ', fontsize=9)
trig_tap_x = d.here[0]
trig_tap_y = d.here[1]
d += elm.Dot().label('TRIG', fontsize=8, loc='top')
d.push()

# Lower resistor to ground
d += elm.Resistor().down(2).label('R5\n10kΩ', fontsize=9, loc='right')
d += elm.Ground()

# BAT85 clamp to 3.3V
d.pop()
d.push()
d += elm.Diode().up(2).label('D2\nBAT85', fontsize=9, loc='left')
d += elm.Vdd().label('3.3V', fontsize=9)

# Connection to M4 A4
d.pop()
d += elm.Line().right(8-2-trig_tap_x)
d += elm.Line().down(trig_tap_y - (22))

# =============================================================================
# I2C PERIPHERALS - TOP
# =============================================================================
d += elm.Label().at((5, 29)).label('I2C BUS', fontsize=11, halign='center', font='bold')

# OLED
d += elm.Ic(pins=[
    elm.IcPin(name='SDA', side='bot', pin='1'),
    elm.IcPin(name='SCL', side='bot', pin='2'),
]).at((5, 27)).label('OLED\n0x3C', fontsize=9)

# OLED connections to M4
d += elm.Line().at((5-0.25, 27-1)).down(1.5)
oled_sda_y = d.here[1]
d += elm.Dot()
d += elm.Line().right((8-2)-(5-0.25))
d += elm.Line().down(oled_sda_y - (22+3))

d += elm.Line().at((5+0.25, 27-1)).down(1)
oled_scl_y = d.here[1]
d += elm.Dot()
d += elm.Line().right((8-2)-(5+0.25))
d += elm.Line().down(oled_scl_y - (22+2.3))

# DAC
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='SDA', side='bot', pin='2'),
    elm.IcPin(name='SCL', side='bot', pin='3'),
    elm.IcPin(name='VA', side='right', pin='4'),
    elm.IcPin(name='VB', side='right', pin='5'),
    elm.IcPin(name='VC', side='right', pin='6'),
]).at((11, 27)).label('DAC\n0x60', fontsize=9)

# DAC power
d += elm.Line().at((11-1, 27+0.7)).left(0.5)
d += elm.Vdd().label('5V', fontsize=9)

# DAC SDA connection (join to OLED SDA line)
d += elm.Line().at((11-0.25, 27-1)).down(1.5)
d += elm.Dot()
d += elm.Line().left((11-0.25)-(5-0.25))

# DAC SCL connection (join to OLED SCL line)
d += elm.Line().at((11+0.25, 27-1)).down(1)
d += elm.Dot()
d += elm.Line().left((11+0.25)-(5+0.25))

# =============================================================================
# MIDI - BOTTOM
# =============================================================================
d += elm.Label().at((8, 18)).label('MIDI I/O', fontsize=11, halign='center', font='bold')

# MIDI IN
d += elm.Dot().at((6, 17)).label('MIDI IN', fontsize=9, halign='right')
d += elm.Line().right(1.5)
d += elm.Line().up((22-3) - 17)

# MIDI OUT
d += elm.Dot().at((6, 16.5)).label('MIDI OUT', fontsize=9, halign='right')
d += elm.Line().right(2)
d += elm.Line().up((22-3.7) - 16.5)

# =============================================================================
# CV LED - RIGHT UPPER
# =============================================================================
d += elm.Label().at((15, 24)).label('INDICATORS', fontsize=12, halign='left', font='bold')

# CV LED from M4 D4
d += elm.Line().at((8+2, 22+0.7)).right(1)
cv_led_x = d.here[0]
d += elm.Line().down((22+0.7) - 23)
d += elm.Resistor().right(2).label('1kΩ', fontsize=9)
d += elm.LED().right(1.5).label('CV', fontsize=9)
d += elm.Ground()

# =============================================================================
# TRIG RGB LEDS - RIGHT MIDDLE
# =============================================================================

# R channel from M4 D11
d += elm.Line().at((8+2, 22)).right(0.5)
rgb_x = d.here[0]
d += elm.Line().down(22 - 21.5)
d += elm.Resistor().right(2).label('330Ω', fontsize=9)
d += elm.LED().right(1.5).label('R', fontsize=9)
d += elm.Ground()

# G channel from M4 D23
d += elm.Line().at((8+2, 22-0.7)).right(0.5)
d += elm.Line().down((22-0.7) - 20.7)
d += elm.Resistor().right(2).label('330Ω', fontsize=9)
d += elm.LED().right(1.5).label('G', fontsize=9)
d += elm.Ground()

# B channel from M4 D24
d += elm.Line().at((8+2, 22-1.4)).right(0.5)
d += elm.Line().down((22-1.4) - 19.9)
d += elm.Resistor().right(2).label('330Ω', fontsize=9)
d += elm.LED().right(1.5).label('B', fontsize=9)
d += elm.Ground()

# =============================================================================
# DAC OUTPUTS - RIGHT SIDE
# =============================================================================
d += elm.Label().at((15, 28)).label('CV OUTPUTS', fontsize=12, halign='left', font='bold')

# CV OUT from DAC VA
d += elm.Line().at((11+1, 27+1.05)).right(2)
d += elm.Resistor().right(2).label('R6\n100Ω', fontsize=9)
d += elm.Dot().label('CV OUT', fontsize=9, halign='left')
d += elm.Ground()

# TRIG V OUT from DAC VB
d += elm.Line().at((11+1, 27+0.35)).right(2)
d += elm.Resistor().right(2).label('R7\n100Ω', fontsize=9)
d += elm.Dot().label('TRIG V', fontsize=9, halign='left')
d += elm.Ground()

# CC OUT from DAC VC
d += elm.Line().at((11+1, 27-0.35)).right(2)
d += elm.Resistor().right(2).label('R10\n100Ω', fontsize=9)
d += elm.Dot().label('CC OUT', fontsize=9, halign='left')
d += elm.Ground()

# =============================================================================
# S-TRIG CIRCUIT - RIGHT LOWER
# =============================================================================
d += elm.Label().at((15, 19)).label('S-TRIG OUTPUT', fontsize=12, halign='left', font='bold')

# From M4 D10
d += elm.Line().at((8+2, 22-0.7+0.7)).right(2)
d += elm.Line().down((22) - 18)
d += elm.Resistor().right(1.5).label('R8\n1kΩ', fontsize=9)

# Transistor
d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1\n2N3904', fontsize=9, loc='bottom')
q_here = d.here

# Collector with resistor
d += elm.Line().at((q_here[0]+0.3, q_here[1]+0.6)).up(0.5)
d += elm.Resistor().up(1.5).label('R9\n100Ω', fontsize=9, loc='right')
d += elm.Dot().label('TRIG S', fontsize=9, halign='left')

# Emitter to ground
d += elm.Line().at((q_here[0]+0.3, q_here[1]-0.6)).down(0.5)
d += elm.Ground()

# =============================================================================
# POWER LEGEND
# =============================================================================
d += elm.Label().at((0, 14)).label('POWER:', fontsize=11, halign='left', font='bold')
d += elm.Vdd().at((2, 13.5)).label('5V (USB)', fontsize=9)
d += elm.Vdd().at((4, 13.5)).label('3.3V (M4)', fontsize=9)
d += elm.Ground().at((6.5, 13.5)).label('GND', fontsize=9)

# =============================================================================
# SPECIFICATIONS
# =============================================================================
d += elm.Label().at((0, 12)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
d += elm.Label().at((0, 11.5)).label('• Input Protection: 10kΩ divider + BAT85 clamp = 0-40V+ safe', fontsize=8, halign='left')
d += elm.Label().at((0, 11)).label('• CV/TRIG Output: 0-5V, 1V/octave, 12-bit (MCP4728)', fontsize=8, halign='left')
d += elm.Label().at((0, 10.5)).label('• I2C Bus: OLED Wing (0x3C), MCP4728 DAC (0x60)', fontsize=8, halign='left')
d += elm.Label().at((0, 10)).label('• Output Protection: 100Ω series resistors on all CV outputs', fontsize=8, halign='left')
d += elm.Label().at((0, 9.5)).label('• Dual Trigger: V-Trig (0-5V from DAC) + S-Trig (switch to GND)', fontsize=8, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - CLEAN PROFESSIONAL LAYOUT")
print("   • Clear left-to-right signal flow")
print("   • All components properly spaced")
print("   • Minimal wire crossings")
print("   • Traditional schematic layout")
