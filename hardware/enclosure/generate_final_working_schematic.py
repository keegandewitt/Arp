#!/usr/bin/env python3
"""
Generate WORKING SCHEMATIC with explicit wire segments
Session 25 - Manual position tracking, every line explicitly drawn
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# Title
d += elm.Label().at((0, 35)).label('PRISME COMPLETE HARDWARE SCHEMATIC', fontsize=18, halign='left', font='bold')

# =============================================================================
# CV IN CIRCUIT (LEFT, TOP)
# =============================================================================
d += elm.Label().at((0, 32)).label('CV IN', fontsize=12, halign='left', font='bold')

# Jack
d += elm.Dot().at((1, 30)).label('Jack', fontsize=9, halign='right')
d.push()
d += elm.Resistor().right(2).label('R1 10kΩ')
cv_tap_pos = d.here
d += elm.Dot().label('TAP', loc='top', fontsize=8)
d.push()

# TAP to M4 A3 - explicit wire
d += elm.Line().right(0.5)
d += elm.Line().up(1)
d += elm.Line().right(4)
d += elm.Line().down(1)
cv_to_a3 = d.here
d += elm.Dot().label('→M4 A3', halign='left', fontsize=8)

# Lower resistor from TAP
d.pop()
d += elm.Resistor().down(1.5).label('R2 10kΩ', loc='right')
d += elm.Ground()

# BAT85 from TAP
d.move_from(cv_tap_pos, dx=0, dy=0)
d += elm.Diode().up(1.5).label('BAT85', loc='left')
d += elm.Vdd().label('3.3V', fontsize=8)

# Jack ground
d.pop()
d += elm.Ground()

# CV LED
d += elm.Dot().at((1, 27)).label('M4 D4', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('1kΩ')
d += elm.LED().right(1).label('CV')
d += elm.Ground()

# =============================================================================
# TRIG IN CIRCUIT (LEFT, MIDDLE)
# =============================================================================
d += elm.Label().at((0, 24)).label('TRIG IN', fontsize=12, halign='left', font='bold')

# Jack
d += elm.Dot().at((1, 22)).label('Jack', fontsize=9, halign='right')
d.push()
d += elm.Resistor().right(2).label('R4 10kΩ')
trig_tap_pos = d.here
d += elm.Dot().label('TAP', loc='top', fontsize=8)
d.push()

# TAP to M4 A4 - explicit wire
d += elm.Line().right(0.5)
d += elm.Line().up(0.5)
d += elm.Line().right(4)
d += elm.Line().down(0.5)
trig_to_a4 = d.here
d += elm.Dot().label('→M4 A4', halign='left', fontsize=8)

# Lower resistor from TAP
d.pop()
d += elm.Resistor().down(1.5).label('R5 10kΩ', loc='right')
d += elm.Ground()

# BAT85 from TAP
d.move_from(trig_tap_pos, dx=0, dy=0)
d += elm.Diode().up(1.5).label('BAT85', loc='left')
d += elm.Vdd().label('3.3V', fontsize=8)

# Jack ground
d.pop()
d += elm.Ground()

# TRIG RGB LED
d += elm.Dot().at((1, 19)).label('M4 D11', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('330Ω')
d += elm.LED().right(1).label('R')
d += elm.Ground()

d += elm.Dot().at((1, 18)).label('M4 D23', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('330Ω')
d += elm.LED().right(1).label('G')
d += elm.Ground()

d += elm.Dot().at((1, 17)).label('M4 D24', fontsize=8, halign='right')
d += elm.Resistor().right(1.5).label('330Ω')
d += elm.LED().right(1).label('B')
d += elm.Ground()

# =============================================================================
# FEATHER M4 (CENTER)
# =============================================================================
d += elm.Label().at((10, 32)).label('FEATHER M4', fontsize=12, halign='center', font='bold')

# M4 block
m4 = elm.Ic(pins=[
    elm.IcPin(name='A3', side='left', pin='1'),
    elm.IcPin(name='A4', side='left', pin='2'),
    elm.IcPin(name='D4', side='right', pin='3'),
    elm.IcPin(name='D10', side='right', pin='4'),
    elm.IcPin(name='D11', side='right', pin='5'),
    elm.IcPin(name='D23', side='right', pin='6'),
    elm.IcPin(name='D24', side='right', pin='7'),
    elm.IcPin(name='SDA', side='top', pin='8'),
    elm.IcPin(name='SCL', side='top', pin='9'),
]).at((10, 25))
d += m4

# Wire CV IN to A3
d += elm.Line().at(cv_to_a3).to((10-2, 25+1.4))

# Wire TRIG IN to A4
d += elm.Line().at(trig_to_a4).to((10-2, 25+0.7))

# =============================================================================
# I2C PERIPHERALS (TOP)
# =============================================================================

# OLED
d += elm.Ic(pins=[
    elm.IcPin(name='SDA', side='bot', pin='1'),
    elm.IcPin(name='SCL', side='bot', pin='2'),
]).at((8, 30)).label('OLED\n0x3C', fontsize=10)

# Connect OLED SDA to M4
d += elm.Line().at((8-0.35, 30-1)).down(1.5)
sda_junction = d.here
d += elm.Dot()
d += elm.Line().right(10-2-8+0.35)
d += elm.Line().down(30-1-1.5-(25+3))

# Connect OLED SCL to M4
d += elm.Line().at((8+0.35, 30-1)).down(1.5)
scl_junction = d.here
d += elm.Dot()
d += elm.Line().right(10-2-8-0.35)
d += elm.Line().down(30-1-1.5-(25+2.3))

# DAC
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='SDA', side='bot', pin='2'),
    elm.IcPin(name='SCL', side='bot', pin='3'),
    elm.IcPin(name='VA', side='right', pin='4'),
    elm.IcPin(name='VB', side='right', pin='5'),
    elm.IcPin(name='VC', side='right', pin='6'),
]).at((12, 30)).label('DAC\n0x60', fontsize=10)

# Connect DAC to 5V
d += elm.Line().at((12-1, 30+0.7)).left(1)
d += elm.Vdd().label('5V', fontsize=9)

# Connect DAC SDA to I2C bus
d += elm.Line().at((12-0.35, 30-1)).down(1.5)
d += elm.Line().to(sda_junction)

# Connect DAC SCL to I2C bus
d += elm.Line().at((12+0.35, 30-1)).down(1.5)
d += elm.Line().to(scl_junction)

# =============================================================================
# MIDI (BOTTOM)
# =============================================================================
d += elm.Label().at((10, 21)).label('MIDI', fontsize=11, halign='center', font='bold')

# MIDI IN
d += elm.Dot().at((8, 20)).label('IN', fontsize=8, halign='right')
d += elm.Line().right(1.5)
d += elm.Line().up(25-3-20)
midi_rx = d.here
d += elm.Dot().label('RX', fontsize=7)

# MIDI OUT
d += elm.Dot().at((8, 19)).label('OUT', fontsize=8, halign='right')
d += elm.Line().right(2)
d += elm.Line().up(25-3.7-19)
midi_tx = d.here
d += elm.Dot().label('TX', fontsize=7)

# =============================================================================
# DAC OUTPUTS (RIGHT)
# =============================================================================
d += elm.Label().at((16, 32)).label('OUTPUTS', fontsize=12, halign='left', font='bold')

# CV OUT
d += elm.Line().at((12+1, 30+1.4)).right(1.5)
d += elm.Resistor().right(2).label('R1 100Ω')
d += elm.Dot().label('CV OUT', halign='left')
d += elm.Ground()

# TRIG OUT V-Trig
d += elm.Line().at((12+1, 30+0.7)).right(1.5)
d += elm.Resistor().right(2).label('R2 100Ω')
d += elm.Dot().label('TRIG V', halign='left')
d += elm.Ground()

# CC OUT
d += elm.Line().at((12+1, 30)).right(1.5)
d += elm.Resistor().right(2).label('R3 100Ω')
d += elm.Dot().label('CC OUT', halign='left')
d += elm.Ground()

# =============================================================================
# S-TRIG (RIGHT BOTTOM)
# =============================================================================
d += elm.Label().at((16, 24)).label('S-TRIG', fontsize=11, halign='left', font='bold')

# From M4 D10
d += elm.Line().at((10+2, 25-0.7)).right(2)
d += elm.Line().down(25-0.7-22)
d += elm.Resistor().right(2).label('R8 1kΩ')
d += elm.Bjt(circle=True).right().anchor('base').label('Q1', loc='bottom')
q_base = d.here

# Collector
d += elm.Line().at((q_base[0]+0.5, q_base[1]+0.8)).up(0.5)
d += elm.Resistor().up(1.5).label('R9 100Ω', loc='right')
d += elm.Dot().label('TRIG S', halign='left')

# Emitter
d += elm.Line().at((q_base[0]+0.5, q_base[1]-0.8)).down(0.5)
d += elm.Ground()

# =============================================================================
# POWER
# =============================================================================
d += elm.Label().at((0, 36)).label('POWER:', fontsize=11, halign='left', font='bold')
d += elm.Vdd().at((2, 35.5)).label('5V USB', fontsize=9)
d += elm.Vdd().at((4, 35.5)).label('3.3V', fontsize=9)
d += elm.Ground().at((6, 35.5)).label('GND', fontsize=9)

# =============================================================================
# NOTES
# =============================================================================
d += elm.Label().at((0, 14)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
d += elm.Label().at((0, 13.5)).label('• Input: 10kΩ divider + BAT85 = 0-40V+ safe', fontsize=8, halign='left')
d += elm.Label().at((0, 13)).label('• Output: 0-5V, 1V/octave, 12-bit (4096 steps)', fontsize=8, halign='left')
d += elm.Label().at((0, 12.5)).label('• I2C: OLED 0x3C, DAC 0x60', fontsize=8, halign='left')
d += elm.Label().at((0, 12)).label('• Protection: 100Ω series on all outputs', fontsize=8, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - EXPLICIT WIRING VERSION")
print("   Every wire segment explicitly drawn with .to() or directional methods")
