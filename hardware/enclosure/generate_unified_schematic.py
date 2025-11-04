#!/usr/bin/env python3
"""
Generate UNIFIED SYSTEM SCHEMATIC - Traditional style with all connections
Session 25 - Shows M4 at center with all peripherals connected
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# Title
d += elm.Label().at((0, 22)).label('PRISME - COMPLETE HARDWARE SCHEMATIC', fontsize=16, halign='left', font='bold')
d += elm.Label().at((0, 21.2)).label('Unified system diagram showing all interconnections', fontsize=11, halign='left')
d += elm.Label().at((0, 20.6)).label('Date: 2025-11-03 | Session 25', fontsize=9, halign='left')

# ============================================================================
# CENTRAL COMPONENT: FEATHER M4 CAN EXPRESS
# ============================================================================

m4_x = 8
m4_y = 14

d += elm.Label().at((m4_x - 2, m4_y + 3)).label('FEATHER M4 CAN EXPRESS', fontsize=14, halign='center', font='bold')
d += elm.Label().at((m4_x - 2, m4_y + 2.5)).label('ATSAMD51 Cortex-M4 @ 120MHz', fontsize=9, halign='center')

# Draw M4 as IC block with pins
d += elm.Ic(pins=[
    # Left side - Power
    elm.IcPin(name='USB', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='3V3', side='left', pin='3'),
    # Left side - I2C
    elm.IcPin(name='SDA', side='left', pin='4'),
    elm.IcPin(name='SCL', side='left', pin='5'),
    # Bottom - ADC
    elm.IcPin(name='A3', side='bot', pin='6'),
    elm.IcPin(name='A4', side='bot', pin='7'),
    # Top - UART
    elm.IcPin(name='RX', side='top', pin='8'),
    elm.IcPin(name='TX', side='top', pin='9'),
    # Right - GPIO
    elm.IcPin(name='D4', side='right', pin='10'),
    elm.IcPin(name='D10', side='right', pin='11'),
    elm.IcPin(name='D11', side='right', pin='12'),
    elm.IcPin(name='D23', side='right', pin='13'),
    elm.IcPin(name='D24', side='right', pin='14'),
]).at((m4_x, m4_y)).label('M4', fontsize=11, loc='center')

# ============================================================================
# POWER DISTRIBUTION (LEFT SIDE)
# ============================================================================

# USB-C Input
usb_in = (1, m4_y + 3)
d += elm.Dot().at(usb_in).label('USB-C\n5V IN', fontsize=9, halign='right')
d += elm.Line().right(1.5)
d += elm.Dot().label('5V', fontsize=8, halign='left')

# Connect to M4 USB pin
d += elm.Line().at((m4_x - 2, m4_y + 3)).left(4.5)

# 5V Rail distribution
five_v_rail = (m4_x - 2, m4_y + 2.3)
d += elm.Line().at(five_v_rail).left(2)
five_v_node = (five_v_rail[0] - 2, five_v_rail[1])
d += elm.Dot().at(five_v_node)
d += elm.Vdd().at((five_v_node[0], five_v_node[1] + 0.5)).label('5V\nRAIL', fontsize=9)

# 5V to DAC (via bottom board decoupling)
d += elm.Line().at(five_v_node).down(0.8)
d += elm.Capacitor().down(1).label('C1 47µF\n+\nC2 0.1µF\n(Bottom)', fontsize=7, loc='left')
d += elm.Line().down(0.5)
dac_5v = (five_v_node[0], five_v_node[1] - 2.3)
d += elm.Dot().at(dac_5v).label('To DAC VDD', fontsize=8, halign='right')

# 5V to top board
d += elm.Line().at(five_v_node).up(0.8)
d += elm.Capacitor().down(1).label('C11 10µF\n+\nC12 0.1µF\n(Top)', fontsize=7, loc='right')

# 3.3V Rail from M4 regulator
three_v_rail = (m4_x - 2, m4_y + 1.5)
d += elm.Line().at(three_v_rail).left(1)
three_v_node = (three_v_rail[0] - 1, three_v_rail[1])
d += elm.Dot().at(three_v_node)
d += elm.Vdd().at((three_v_node[0], three_v_node[1] + 0.5)).label('3.3V\nRAIL', fontsize=9)

# 3.3V to peripherals
d += elm.Line().at(three_v_node).down(0.8)
d += elm.Capacitor().down(1).label('C9 10µF\n+\nC10 0.1µF\n(Bottom)', fontsize=7, loc='left')

d += elm.Line().at(three_v_node).up(0.8)
d += elm.Capacitor().down(1).label('C13 10µF\n+\nC14 0.1µF\n(Top)', fontsize=7, loc='right')

# Ground
gnd_pin = (m4_x - 2, m4_y + 2.3 - 0.7)
d += elm.Line().at(gnd_pin).left(0.8)
d += elm.Ground().label('GND', fontsize=8)

# ============================================================================
# I2C BUS (LEFT SIDE - SHARED)
# ============================================================================

# SDA line
sda_pin = (m4_x - 2, m4_y + 0.8)
d += elm.Line().at(sda_pin).left(3.5)
sda_bus = (sda_pin[0] - 3.5, sda_pin[1])
d += elm.Dot().at(sda_bus).label('SDA\nBUS', fontsize=9, halign='right')

# SDA to OLED
d += elm.Line().at(sda_bus).up(3)
d += elm.Dot().label('OLED\n0x3C', fontsize=8, halign='right')

# SDA to DAC
d += elm.Line().at(sda_bus).down(3)
d += elm.Dot().label('DAC\n0x60', fontsize=8, halign='right')

# SCL line
scl_pin = (m4_x - 2, m4_y + 0.1)
d += elm.Line().at(scl_pin).left(3)
scl_bus = (scl_pin[0] - 3, scl_pin[1])
d += elm.Dot().at(scl_bus).label('SCL\nBUS', fontsize=9, halign='right')

# SCL to OLED
d += elm.Line().at(scl_bus).up(3.7)
d += elm.Dot()

# SCL to DAC
d += elm.Line().at(scl_bus).down(2.3)
d += elm.Dot()

# ============================================================================
# OLED WING (TOP LEFT)
# ============================================================================

oled_x = 3
oled_y = m4_y + 5

d += elm.Ic(pins=[
    elm.IcPin(name='3V3', side='left', pin='1'),
    elm.IcPin(name='SDA', side='bot', pin='2'),
    elm.IcPin(name='SCL', side='bot', pin='3'),
]).at((oled_x, oled_y)).label('OLED\nWing\n128x64\n0x3C', fontsize=8, loc='center')

# Power
d += elm.Line().at((oled_x - 1, oled_y + 0.7)).left(0.5)
d += elm.Vdd().label('3.3V', fontsize=7)

# ============================================================================
# UART - MIDI WING (TOP CENTER)
# ============================================================================

# RX line
rx_pin = (m4_x - 2, m4_y + 4)
d += elm.Line().at(rx_pin).up(2)
d += elm.Dot().label('MIDI\nIN', fontsize=8, halign='left')

# TX line
tx_pin = (m4_x - 2, m4_y + 4 + 0.7)
d += elm.Line().at(tx_pin).up(1.3)
d += elm.Dot().label('MIDI\nOUT', fontsize=8, halign='left')

d += elm.Label().at((m4_x - 1, m4_y + 6.5)).label('MIDI Wing', fontsize=10, halign='center', font='bold')
d += elm.Label().at((m4_x - 1, m4_y + 6)).label('DIN-5 I/O', fontsize=8, halign='center')
d += elm.Label().at((m4_x - 1, m4_y + 5.6)).label('3.3V power', fontsize=7, halign='center')

# ============================================================================
# ADC INPUTS - CV IN (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((2, m4_y - 3)).label('CV IN CIRCUIT', fontsize=11, halign='center', font='bold')

# CV IN Jack
cv_jack = (1, m4_y - 4)
d += elm.Dot().at(cv_jack).label('CV IN\nJack', fontsize=8, halign='right')

# Voltage divider
d += elm.Line().right(0.8)
d += elm.Resistor().right(1.5).label('R1\n10kΩ', fontsize=7, loc='top')

cv_tap = (cv_jack[0] + 2.3, cv_jack[1])
d += elm.Dot().at(cv_tap).label('TAP', fontsize=7, loc='top')

# Lower resistor to GND
d += elm.Line().at(cv_tap).down(0.5)
d += elm.Resistor().down(1).label('R2\n10kΩ', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# BAT85 to 3.3V
d += elm.Line().at(cv_tap).up(0.5)
d += elm.Diode().up(1).label('D1\nBAT85', fontsize=7, loc='left')
d += elm.Line().up(0.3)
d += elm.Vdd().label('3.3V', fontsize=7)

# To M4 A3
d += elm.Line().at(cv_tap).right(2)
a3_node = (cv_tap[0] + 2, cv_tap[1])
d += elm.Dot().at(a3_node)
d += elm.Line().up(m4_y - 2 - a3_node[1])

# Jack ground
d += elm.Line().at(cv_jack).down(0.5)
d += elm.Ground()

# CV LED
d += elm.Line().at((cv_jack[0], cv_jack[1] - 2)).right(0.3)
d += elm.Dot().label('D4→', fontsize=7, halign='right')
d += elm.Line().right(0.5)
d += elm.Resistor().right(1.5).label('R3 1kΩ', fontsize=7, loc='top')
d += elm.Line().right(0.3)
d += elm.LED().right(1).label('LED1', fontsize=7, loc='top')
d += elm.Line().right(0.3)
d += elm.Ground()

# ============================================================================
# ADC INPUTS - TRIG IN (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((2, m4_y - 7)).label('TRIG IN CIRCUIT', fontsize=11, halign='center', font='bold')

# TRIG IN Jack
trig_jack = (1, m4_y - 8)
d += elm.Dot().at(trig_jack).label('TRIG IN\nJack', fontsize=8, halign='right')

# Voltage divider
d += elm.Line().right(0.8)
d += elm.Resistor().right(1.5).label('R4\n10kΩ', fontsize=7, loc='top')

trig_tap = (trig_jack[0] + 2.3, trig_jack[1])
d += elm.Dot().at(trig_tap).label('TAP', fontsize=7, loc='top')

# Lower resistor to GND
d += elm.Line().at(trig_tap).down(0.5)
d += elm.Resistor().down(1).label('R5\n10kΩ', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# BAT85 to 3.3V
d += elm.Line().at(trig_tap).up(0.5)
d += elm.Diode().up(1).label('D2\nBAT85', fontsize=7, loc='left')
d += elm.Line().up(0.3)
d += elm.Vdd().label('3.3V', fontsize=7)

# To M4 A4
d += elm.Line().at(trig_tap).right(2)
a4_node = (trig_tap[0] + 2, trig_tap[1])
d += elm.Dot().at(a4_node)
d += elm.Line().up(m4_y - 2 - 0.7 - a4_node[1])

# Jack ground
d += elm.Line().at(trig_jack).down(0.5)
d += elm.Ground()

# TRIG RGB LED (simplified - show as one block)
d += elm.Label().at((1, trig_jack[1] - 2)).label('D11,D23,D24→', fontsize=7, halign='right')
d += elm.Line().at((2, trig_jack[1] - 2)).right(0.5)
d += elm.Resistor().right(1).label('330Ω', fontsize=7, loc='top')
d += elm.Line().right(0.3)
d += elm.LED().right(1).label('RGB', fontsize=7, loc='top')
d += elm.Line().right(0.3)
d += elm.Ground()

# ============================================================================
# MCP4728 DAC (BOTTOM RIGHT)
# ============================================================================

dac_x = m4_x + 4
dac_y = m4_y - 3

d += elm.Label().at((dac_x, dac_y + 2)).label('MCP4728 DAC', fontsize=11, halign='center', font='bold')

d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='SDA', side='left', pin='2'),
    elm.IcPin(name='SCL', side='left', pin='3'),
    elm.IcPin(name='VA', side='right', pin='4'),
    elm.IcPin(name='VB', side='right', pin='5'),
    elm.IcPin(name='VC', side='right', pin='6'),
]).at((dac_x, dac_y)).label('0x60', fontsize=8, loc='center')

# Power - connect to 5V node on left
d += elm.Line().at((dac_x - 1, dac_y + 1.5)).left(1.5)
d += elm.Line().up(dac_5v[1] - (dac_y + 1.5))
d += elm.Line().left(dac_x - 1 - 1.5 - five_v_node[0])

# I2C - connect to bus
d += elm.Line().at((dac_x - 1, dac_y + 0.8)).left(1)
d += elm.Line().up(sda_bus[1] - (dac_y + 0.8))
d += elm.Line().left(0.5)

d += elm.Line().at((dac_x - 1, dac_y + 0.1)).left(0.5)
d += elm.Line().up(scl_bus[1] - (dac_y + 0.1))
d += elm.Line().left(1)

# GND
d += elm.Line().at((dac_x - 1, dac_y - 0.6)).left(0.5)
d += elm.Ground()

# Channel A - CV OUT
d += elm.Line().at((dac_x + 1, dac_y + 1.5)).right(0.5)
d += elm.Resistor().right(1.5).label('R1 100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CV OUT\nJack', fontsize=8, halign='left')
d += elm.Line().at((dac_x + 1 + 2.5, dac_y + 1.5)).down(0.5)
d += elm.Ground()

# Channel B - TRIG OUT (V-Trig)
d += elm.Line().at((dac_x + 1, dac_y + 0.8)).right(0.5)
d += elm.Resistor().right(1.5).label('R2 100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('TRIG OUT\nJack\n(V-Trig)', fontsize=7, halign='left')
d += elm.Line().at((dac_x + 1 + 2.5, dac_y + 0.8)).down(0.5)
d += elm.Ground()

# Channel C - CC OUT
d += elm.Line().at((dac_x + 1, dac_y + 0.1)).right(0.5)
d += elm.Resistor().right(1.5).label('R3 100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Dot().label('CC OUT\nJack', fontsize=8, halign='left')
d += elm.Line().at((dac_x + 1 + 2.5, dac_y + 0.1)).down(0.5)
d += elm.Ground()

# ============================================================================
# S-TRIG CIRCUIT (RIGHT SIDE)
# ============================================================================

d += elm.Label().at((dac_x, dac_y - 3.5)).label('S-TRIG CIRCUIT', fontsize=11, halign='center', font='bold')

# From M4 D10
d10_start = (m4_x + 2, m4_y + 0.8)
d += elm.Line().at(d10_start).right(0.5)
d += elm.Line().down(d10_start[1] - (dac_y - 4.5))
d10_node = (d10_start[0] + 0.5, dac_y - 4.5)

# Base resistor
d += elm.Line().at(d10_node).right(0.5)
d += elm.Resistor().right(1.5).label('R8 1kΩ', fontsize=7, loc='top')

# Transistor
q_pos = (d10_node[0] + 2, d10_node[1])
d += elm.Bjt(circle=True).at(q_pos).label('Q1\n2N3904', fontsize=7, loc='bottom')

# Collector to jack
d += elm.Line().at((q_pos[0], q_pos[1] + 0.7)).up(0.5)
d += elm.Resistor().up(1).label('R9\n100Ω', fontsize=7, loc='right')
d += elm.Line().up(0.5)
d += elm.Dot().label('TRIG OUT\nJack\n(S-Trig)', fontsize=7, halign='left')

# Emitter to GND
d += elm.Line().at((q_pos[0], q_pos[1] - 0.7)).down(0.5)
d += elm.Ground()

# ============================================================================
# LEGEND / NOTES
# ============================================================================

d += elm.Label().at((0, m4_y - 12)).label('SYSTEM OVERVIEW:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((0, m4_y - 12.6)).label('• M4 at center with all peripherals connected via actual signal paths', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 13)).label('• Power rails (5V, 3.3V) distributed from M4 to all components', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 13.4)).label('• I2C bus shared between OLED (0x3C) and DAC (0x60)', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 13.8)).label('• Top PCB: CV IN + TRIG IN circuits (left side)', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 14.2)).label('• Bottom PCB: DAC outputs + S-Trig circuit (right side)', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 14.6)).label('• MIDI Wing: UART connection (top)', fontsize=8, halign='left')
d += elm.Label().at((0, m4_y - 15)).label('• OLED Wing: I2C connection (top left)', fontsize=8, halign='left')

d += elm.Label().at((10, m4_y - 12)).label('KEY SPECIFICATIONS:', fontsize=12, halign='left', font='bold')
d += elm.Label().at((10, m4_y - 12.6)).label('Input Protection: 10kΩ divider + BAT85 (safe 0-40V+)', fontsize=8, halign='left')
d += elm.Label().at((10, m4_y - 13)).label('Output Range: 0-5V (5 octaves, 1V/octave)', fontsize=8, halign='left')
d += elm.Label().at((10, m4_y - 13.4)).label('DAC Resolution: 12-bit (4096 steps)', fontsize=8, halign='left')
d += elm.Label().at((10, m4_y - 13.8)).label('I2C Addresses: OLED 0x3C, DAC 0x60', fontsize=8, halign='left')
d += elm.Label().at((10, m4_y - 14.2)).label('Trigger Modes: V-Trig (0-5V) or S-Trig (switch)', fontsize=8, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg saved")
print("\n📐 Traditional schematic with M4 at center and all components interconnected")
print("   - Shows actual signal paths and connections")
print("   - Power distribution visible")
print("   - I2C bus sharing shown")
print("   - All inputs and outputs connected")
