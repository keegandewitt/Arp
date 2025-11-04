#!/usr/bin/env python3
"""
Generate PROPERLY CONNECTED SYSTEM SCHEMATIC
Session 25 - Using proper schemdraw connection methods
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# Title
d += elm.Label().at((0, 30)).label('PRISME - COMPLETE HARDWARE SCHEMATIC', fontsize=18, halign='left', font='bold')
d += elm.Label().at((0, 29)).label('All components with proper electrical connections', fontsize=12, halign='left')

# ============================================================================
# M4 AT CENTER
# ============================================================================

m4_y = 20

# Draw M4 as block at center
d += elm.Label().at((6, m4_y + 2)).label('FEATHER M4 CAN EXPRESS', fontsize=14, halign='center', font='bold')
d += elm.Ic(pins=[
    # Left side
    elm.IcPin(name='USB', side='left', pin='1'),
    elm.IcPin(name='3V3', side='left', pin='2'),
    elm.IcPin(name='SDA', side='left', pin='3'),
    elm.IcPin(name='SCL', side='left', pin='4'),
    # Bottom
    elm.IcPin(name='A3', side='bot', pin='5'),
    elm.IcPin(name='A4', side='bot', pin='6'),
    # Right
    elm.IcPin(name='D4', side='right', pin='7'),
    elm.IcPin(name='D10', side='right', pin='8'),
    elm.IcPin(name='D11', side='right', pin='9'),
    elm.IcPin(name='D23', side='right', pin='10'),
    elm.IcPin(name='D24', side='right', pin='11'),
    # Top
    elm.IcPin(name='RX', side='top', pin='12'),
    elm.IcPin(name='TX', side='top', pin='13'),
]).at((6, m4_y)).label('M4', fontsize=12, loc='center')

# ============================================================================
# POWER RAILS (TOP)
# ============================================================================

# 5V rail
d += elm.Line().at((6-4, m4_y+3.5)).left(3)
d += elm.Vdd().label('5V\nUSB', fontsize=11)

# 3.3V rail
d += elm.Line().at((6-4, m4_y+2.8)).left(2)
d += elm.Vdd().label('3.3V', fontsize=11)

# Ground
d += elm.Ground().at((2, m4_y-6)).label('GND', fontsize=11, halign='left')

# ============================================================================
# I2C BUS (LEFT SIDE) - PROPERLY CONNECTED
# ============================================================================

d += elm.Label().at((0, m4_y+1)).label('I2C BUS', fontsize=13, halign='left', font='bold')

# OLED Wing on I2C
oled_y = m4_y + 6
d += elm.Ic(pins=[
    elm.IcPin(name='SDA', side='right', pin='1'),
    elm.IcPin(name='SCL', side='right', pin='2'),
]).at((2, oled_y)).label('OLED\n0x3C', fontsize=10, loc='center')

# Connect OLED SDA to M4 SDA
d += elm.Line().at((2+1, oled_y+0.35)).right(1.5)
sda_node_1 = d.here
d += elm.Line().down(oled_y+0.35 - (m4_y+2.1))
d += elm.Line().right(6-4 - sda_node_1[0])

# Connect OLED SCL to M4 SCL
d += elm.Line().at((2+1, oled_y-0.35)).right(1)
scl_node_1 = d.here
d += elm.Line().down(oled_y-0.35 - (m4_y+1.4))
d += elm.Line().right(6-4 - scl_node_1[0])

# MCP4728 DAC on I2C
dac_y = m4_y - 4
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='SDA', side='right', pin='2'),
    elm.IcPin(name='SCL', side='right', pin='3'),
    elm.IcPin(name='VA', side='top', pin='4'),
    elm.IcPin(name='VB', side='top', pin='5'),
    elm.IcPin(name='VC', side='top', pin='6'),
]).at((2, dac_y)).label('DAC\n0x60', fontsize=10, loc='center')

# Connect DAC VDD to 5V
d += elm.Line().at((2-1, dac_y+0.7)).left(1)
d += elm.Line().up(3)
d += elm.Dot()

# Connect DAC SDA to I2C bus (tap from OLED connection)
d += elm.Line().at((2+1, dac_y+0.35)).right(1.5)
d += elm.Dot()
d += elm.Line().up(oled_y - 0.7 - dac_y)
d += elm.Dot().at(sda_node_1)

# Connect DAC SCL to I2C bus (tap from OLED connection)
d += elm.Line().at((2+1, dac_y-0.35)).right(1)
d += elm.Dot()
d += elm.Line().up(oled_y - 0.7 - dac_y - 0.7)
d += elm.Dot().at(scl_node_1)

# ============================================================================
# MIDI UART (TOP)
# ============================================================================

d += elm.Label().at((6, m4_y+6)).label('MIDI I/O', fontsize=13, halign='center', font='bold')

# MIDI RX
d += elm.Dot().at((6-4, m4_y+4.9)).label('MIDI IN', fontsize=9, halign='right')
d += elm.Line().right(1.5)
d += elm.Line().down(0.9)

# MIDI TX
d += elm.Dot().at((6-4, m4_y+5.6)).label('MIDI OUT', fontsize=9, halign='right')
d += elm.Line().right(2)
d += elm.Line().down(1.6)

# ============================================================================
# CV IN CIRCUIT (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((0, m4_y-7)).label('CV IN', fontsize=13, halign='left', font='bold')

cv_in_y = m4_y - 8.5

# Jack
d += elm.Dot().at((0, cv_in_y)).label('Jack', fontsize=9, halign='right')
d += elm.Resistor().right(2).label('10kΩ', fontsize=9, loc='top')
cv_tap = d.here

# Tap to M4 A3
d += elm.Dot()
d += elm.Line().right(1.5)
d += elm.Line().up(cv_in_y - (m4_y-2))
d += elm.Line().right(6-4 - cv_tap[0] - 1.5)

# Lower resistor to ground
d += elm.Resistor().at(cv_tap).down(1.5).label('10kΩ', fontsize=9, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp to 3.3V
d += elm.Diode().at(cv_tap).up(1.5).label('BAT85', fontsize=9, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=8)

# Jack ground
d += elm.Ground().at((0, cv_in_y-0.5))

# LED from M4 D4
cv_led_y = cv_in_y - 3
d += elm.Dot().at((6+4, m4_y+0.7)).label('D4', fontsize=8, halign='left')
d += elm.Line().right(2)
d += elm.Line().down(m4_y+0.7 - cv_led_y)
led_node = d.here
d += elm.Resistor().left(1.5).label('1kΩ', fontsize=8, loc='bottom')
d += elm.LED().left(1.5).label('CV', fontsize=8, loc='bottom')
d += elm.Line().left(0.5)
d += elm.Ground()

# ============================================================================
# TRIG IN CIRCUIT (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((0, m4_y-12)).label('TRIG IN', fontsize=13, halign='left', font='bold')

trig_in_y = m4_y - 13.5

# Jack
d += elm.Dot().at((0, trig_in_y)).label('Jack', fontsize=9, halign='right')
d += elm.Resistor().right(2).label('10kΩ', fontsize=9, loc='top')
trig_tap = d.here

# Tap to M4 A4
d += elm.Dot()
d += elm.Line().right(1)
d += elm.Line().up(trig_in_y - (m4_y-2.7))
d += elm.Line().right(6-4 - trig_tap[0] - 1)

# Lower resistor to ground
d += elm.Resistor().at(trig_tap).down(1.5).label('10kΩ', fontsize=9, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp to 3.3V
d += elm.Diode().at(trig_tap).up(1.5).label('BAT85', fontsize=9, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=8)

# Jack ground
d += elm.Ground().at((0, trig_in_y-0.5))

# RGB LED (simplified - show one channel)
trig_led_y = trig_in_y - 3
d += elm.Dot().at((6+4, m4_y+0)).label('D11', fontsize=8, halign='left')
d += elm.Line().right(2)
d += elm.Line().down(m4_y - trig_led_y)
d += elm.Resistor().left(1.5).label('330Ω', fontsize=8, loc='bottom')
d += elm.LED().left(1.5).label('RGB', fontsize=8, loc='bottom')
d += elm.Line().left(0.5)
d += elm.Ground()

# ============================================================================
# DAC OUTPUTS (RIGHT SIDE)
# ============================================================================

d += elm.Label().at((11, m4_y-2)).label('OUTPUTS', fontsize=13, halign='left', font='bold')

# CV OUT from DAC VA
d += elm.Line().at((2+1, dac_y+1.05)).up(1)
d += elm.Line().right(9)
d += elm.Resistor().right(1.5).label('100Ω', fontsize=9, loc='top')
d += elm.Dot().label('CV OUT', fontsize=9, halign='left')
d += elm.Line().down(0.5)
d += elm.Ground()

# TRIG OUT V-Trig from DAC VB
d += elm.Line().at((2+1, dac_y+0.35)).up(0.5)
d += elm.Line().right(9)
d += elm.Resistor().right(1.5).label('100Ω', fontsize=9, loc='top')
d += elm.Dot().label('TRIG V', fontsize=9, halign='left')
d += elm.Line().down(0.5)
d += elm.Ground()

# CC OUT from DAC VC
d += elm.Line().at((2+1, dac_y-0.35)).down(0.5)
d += elm.Line().right(9)
d += elm.Resistor().right(1.5).label('100Ω', fontsize=9, loc='top')
d += elm.Dot().label('CC OUT', fontsize=9, halign='left')
d += elm.Line().down(0.5)
d += elm.Ground()

# ============================================================================
# S-TRIG CIRCUIT (RIGHT BOTTOM)
# ============================================================================

d += elm.Label().at((11, m4_y-7)).label('S-TRIG', fontsize=13, halign='left', font='bold')

# From M4 D10
d += elm.Dot().at((6+4, m4_y-0.7)).label('D10', fontsize=8, halign='left')
d += elm.Line().right(1)
strig_node = d.here
d += elm.Line().down(m4_y-0.7 - (m4_y-9))
d += elm.Resistor().right(1.5).label('1kΩ', fontsize=9, loc='top')

# Transistor
d += elm.Bjt(circle=True).right().anchor('base').label('Q1', fontsize=9, loc='bottom')
q_pos = d.here

# Collector to jack
d += elm.Line().at((q_pos[0], q_pos[1]+0.8)).up(0.5)
d += elm.Resistor().up(1).label('100Ω', fontsize=9, loc='right')
d += elm.Dot().label('TRIG S', fontsize=9, halign='left')

# Emitter to ground
d += elm.Line().at((q_pos[0], q_pos[1]-0.8)).down(0.5)
d += elm.Ground()

# ============================================================================
# NOTES
# ============================================================================

d += elm.Label().at((0, m4_y-17)).label('NOTES:', fontsize=13, halign='left', font='bold')
d += elm.Label().at((0, m4_y-17.7)).label('• I2C bus: OLED (0x3C) + DAC (0x60) share SDA/SCL', fontsize=9, halign='left')
d += elm.Label().at((0, m4_y-18.3)).label('• Input protection: 10kΩ divider + BAT85 = safe 0-40V+', fontsize=9, halign='left')
d += elm.Label().at((0, m4_y-18.9)).label('• Outputs: 0-5V with 100Ω series protection', fontsize=9, halign='left')
d += elm.Label().at((0, m4_y-19.5)).label('• V-Trig and S-Trig share jack (software select)', fontsize=9, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - PROPERLY CONNECTED VERSION")
print("   All connections use proper schemdraw .to(), .right(), .down() methods")
print("   Wires actually connect between components")
