#!/usr/bin/env python3
"""
Generate BOTTOM BOARD (Output) Schematic - ACTUAL Design
Session 25 - Truth-based schematic for EasyEDA PCB design
"""

import schemdraw
import schemdraw.elements as elm

# Create new drawing
d = schemdraw.Drawing()

# Title block
d += elm.Label().at((0, 11)).label('PRISME BOTTOM BOARD - OUTPUT CIRCUITS', fontsize=14, halign='left')
d += elm.Label().at((0, 10.5)).label('Session 25 - Actual Design (0-5V, No Op-Amp)', fontsize=10, halign='left')
d += elm.Label().at((0, 10)).label('Date: 2025-11-03', fontsize=8, halign='left')

# ============================================================================
# SECTION 1: POWER DISTRIBUTION (Both Rails - CRITICAL!)
# ============================================================================

d += elm.Label().at((0, 9)).label('POWER DISTRIBUTION', fontsize=12, halign='left', font='bold')

# 5V Rail (from USB via M4)
d += elm.Label().at((0, 8)).label('5V Rail (Powers DAC):', fontsize=10, halign='left')
d += elm.Vdd().at((3, 8)).label('5V USB\n(from M4)', fontsize=8)
pos_5v = (3, 8)

# 5V bulk capacitor
d += elm.Line().at(pos_5v).down(0.5)
d += elm.Capacitor().down(1).label('C1\n47uF\nElectrolytic', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# 5V bypass capacitor
d += elm.Line().at((3, 7.5)).right(1)
d += elm.Capacitor().down(1).label('C2\n0.1uF\nCeramic', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# 5V to DAC
d += elm.Line().at((3, 8)).right(2)
d += elm.Dot().label('To MCP4728\nVDD', fontsize=7, halign='left')

# 3.3V Rail (from M4 regulator)
d += elm.Label().at((7, 8)).label('3.3V Rail (Powers MIDI/OLED/LEDs):', fontsize=10, halign='left')
d += elm.Vdd().at((12, 8)).label('3.3V\n(from M4)', fontsize=8)
pos_3v3 = (12, 8)

# 3.3V bulk capacitor
d += elm.Line().at(pos_3v3).down(0.5)
d += elm.Capacitor().down(1).label('C9\n10uF\nElectrolytic', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# 3.3V bypass capacitor
d += elm.Line().at((12, 7.5)).right(1)
d += elm.Capacitor().down(1).label('C10\n0.1uF\nCeramic', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# 3.3V to peripherals
d += elm.Line().at((12, 8)).right(2)
d += elm.Dot().label('To MIDI\nOLED\nLEDs', fontsize=7, halign='left')

# ============================================================================
# SECTION 2: MCP4728 I2C DAC
# ============================================================================

d += elm.Label().at((0, 5.5)).label('MCP4728 4-CHANNEL I2C DAC', fontsize=12, halign='left', font='bold')

# DAC chip representation
d += elm.Ic(pins=[
    elm.IcPin(name='VDD', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='SDA', side='left', pin='3'),
    elm.IcPin(name='SCL', side='left', pin='4'),
    elm.IcPin(name='VA', side='right', pin='5'),
    elm.IcPin(name='VB', side='right', pin='6'),
    elm.IcPin(name='VC', side='right', pin='7'),
    elm.IcPin(name='VD', side='right', pin='8')
]).at((2, 4.5)).label('MCP4728\n0x60', fontsize=9, loc='center')

dac_pos = (2, 4.5)

# Power connections
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] + 1.5)).left(0.5)
d += elm.Vdd().label('5V', fontsize=7)

d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] + 0.5)).left(0.5)
d += elm.Ground()

# I2C connections
d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] - 0.5)).left(1.5)
d += elm.Dot().label('To M4\nSDA', fontsize=7, halign='right')

d += elm.Line().at((dac_pos[0] - 1, dac_pos[1] - 1.5)).left(1.5)
d += elm.Dot().label('To M4\nSCL', fontsize=7, halign='right')

# ============================================================================
# SECTION 3: CV OUT (Channel A - 0-5V Direct)
# ============================================================================

d += elm.Label().at((6, 5)).label('CV OUT - 0-5V (1V/octave)', fontsize=10, halign='left')

# From VA pin
va_out = (dac_pos[0] + 1, dac_pos[1] + 1.5)
d += elm.Line().at(va_out).right(1)

# Series protection resistor
d += elm.Resistor().right(1.5).label('R1\n100 ohm', fontsize=7, loc='top')
cv_out = (va_out[0] + 2.5, va_out[1])

# To jack
d += elm.Line().at(cv_out).right(0.5)
d += elm.Dot().label('CV OUT\nJack TIP', fontsize=8, halign='left')

# Jack ground
d += elm.Line().at(cv_out).down(1)
d += elm.Dot().label('Jack\nSLEEVE', fontsize=7, halign='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# LED indicator
d += elm.Line().at((cv_out[0], cv_out[1])).down(2)
d += elm.Resistor().down(0.8).label('R7\n1k ohm', fontsize=7, loc='left')
d += elm.LED().down(0.8).label('LED3\nWhite', fontsize=7, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 4: TRIG OUT V-Trig (Channel B - 0-5V Gate)
# ============================================================================

d += elm.Label().at((6, 2)).label('TRIG OUT (V-Trig) - 0-5V Gate', fontsize=10, halign='left')

# From VB pin
vb_out = (dac_pos[0] + 1, dac_pos[1] + 0.5)
d += elm.Line().at(vb_out).right(1)

# Series protection resistor
d += elm.Resistor().right(1.5).label('R2\n100 ohm', fontsize=7, loc='top')
trig_v_out = (vb_out[0] + 2.5, vb_out[1])

# To jack
d += elm.Line().at(trig_v_out).right(0.5)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(V-Trig)', fontsize=7, halign='left')

# Jack ground
d += elm.Line().at(trig_v_out).down(1)
d += elm.Dot().label('Jack\nSLEEVE', fontsize=7, halign='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 5: TRIG OUT S-Trig (GPIO D10 via Transistor)
# ============================================================================

d += elm.Label().at((6, -1)).label('TRIG OUT (S-Trig) - Switch to GND', fontsize=10, halign='left')

# From GPIO D10
d += elm.Dot().at((6, -2)).label('From M4\nPin D10', fontsize=7, halign='right')
d10_pos = (6, -2)

# Base resistor
d += elm.Line().at(d10_pos).right(0.5)
d += elm.Resistor().right(1.5).label('R8\n1k ohm', fontsize=7, loc='top')

# NPN transistor (2N3904)
transistor_pos = (8, -2)
d += elm.Bjt(circle=True).at(transistor_pos).label('Q1\n2N3904\nNPN', fontsize=7, loc='bottom')

# Collector to jack via series resistor
d += elm.Line().at((transistor_pos[0], transistor_pos[1] + 0.8)).up(0.5)
d += elm.Resistor().up(1).label('R9\n100 ohm', fontsize=7, loc='right')
d += elm.Line().up(0.5)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(S-Trig)', fontsize=7, halign='left')

# Emitter to ground
d += elm.Line().at((transistor_pos[0], transistor_pos[1] - 0.8)).down(0.5)
d += elm.Ground()

# Jack ground (shared with V-Trig)
d += elm.Label().at((9, -0.5)).label('(Same jack as V-Trig,\nuser selects mode)', fontsize=6, halign='left')

# RGB LED indicator
d += elm.Line().at((transistor_pos[0] + 1, transistor_pos[1])).right(1)
d += elm.Resistor().down(0.8).label('R10\n330 ohm', fontsize=7, loc='left')
d += elm.LED().down(0.8).label('LED4\nRGB', fontsize=7, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 6: CC OUT (Channel C - 0-5V MIDI CC)
# ============================================================================

d += elm.Label().at((6, -4)).label('CC OUT - 0-5V (MIDI CC)', fontsize=10, halign='left')

# From VC pin
vc_out = (dac_pos[0] + 1, dac_pos[1] - 0.5)
d += elm.Line().at(vc_out).right(1)

# Series protection resistor
d += elm.Resistor().right(1.5).label('R3\n100 ohm', fontsize=7, loc='top')
cc_out = (vc_out[0] + 2.5, vc_out[1])

# To jack
d += elm.Line().at(cc_out).right(0.5)
d += elm.Dot().label('CC OUT\nJack TIP', fontsize=8, halign='left')

# Jack ground
d += elm.Line().at(cc_out).down(1)
d += elm.Dot().label('Jack\nSLEEVE', fontsize=7, halign='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# LED indicator
d += elm.Line().at((cc_out[0], cc_out[1])).down(2)
d += elm.Resistor().down(0.8).label('R11\n1k ohm', fontsize=7, loc='left')
d += elm.LED().down(0.8).label('LED5\nWhite', fontsize=7, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 7: Channel D (Future Expansion)
# ============================================================================

d += elm.Label().at((6, -7)).label('Channel D - FUTURE (Available)', fontsize=10, halign='left')

# From VD pin
vd_out = (dac_pos[0] + 1, dac_pos[1] - 1.5)
d += elm.Line().at(vd_out).right(1)

# Series protection resistor (footprint)
d += elm.Resistor().right(1.5).label('R4\n100 ohm\n(future)', fontsize=7, loc='top')
d_out = (vd_out[0] + 2.5, vd_out[1])

# To expansion jack (not populated)
d += elm.Line().at(d_out).right(0.5)
d += elm.Dot().label('Future\nExpansion', fontsize=7, halign='left')

# ============================================================================
# SECTION 8: USB-C Power Input
# ============================================================================

d += elm.Label().at((0, -5)).label('USB-C POWER INPUT', fontsize=10, halign='left', font='bold')
d += elm.Dot().at((0, -6)).label('USB-C\n5V', fontsize=7, halign='right')
d += elm.Line().right(1)
d += elm.Vdd().label('5V', fontsize=7)

d += elm.Dot().at((0, -6.5)).label('USB-C\nGND', fontsize=7, halign='right')
d += elm.Line().right(0.5)
d += elm.Ground()

# ============================================================================
# SECTION 9: MIDI FeatherWing Connections
# ============================================================================

d += elm.Label().at((0, -7.5)).label('MIDI CONNECTIONS', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -8)).label('MIDI IN: Via MIDI FeatherWing DIN-5', fontsize=8, halign='left')
d += elm.Label().at((0, -8.5)).label('MIDI OUT: Via MIDI FeatherWing DIN-5', fontsize=8, halign='left')
d += elm.Label().at((0, -9)).label('Power: 3.3V from M4', fontsize=8, halign='left')
d += elm.Label().at((0, -9.5)).label('UART: RX/TX to M4 Serial1', fontsize=8, halign='left')

# ============================================================================
# SECTION 10: Design Notes
# ============================================================================

d += elm.Label().at((0, -11)).label('DESIGN NOTES:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -11.5)).label('1. CV OUT is 0-5V DIRECT (no op-amp, 5 octaves at 1V/octave)', fontsize=8, halign='left')
d += elm.Label().at((0, -12)).label('2. All DAC outputs have 100 ohm series protection', fontsize=8, halign='left')
d += elm.Label().at((0, -12.5)).label('3. TRIG OUT supports V-Trig (DAC) OR S-Trig (transistor)', fontsize=8, halign='left')
d += elm.Label().at((0, -13)).label('4. MCP4728 powered by 5V for full 0-5V output range', fontsize=8, halign='left')
d += elm.Label().at((0, -13.5)).label('5. MIDI + OLED + LEDs powered by 3.3V rail', fontsize=8, halign='left')
d += elm.Label().at((0, -14)).label('6. Both power rails require proper decoupling (C1,C2 + C9,C10)', fontsize=8, halign='left')

d += elm.Label().at((7, -11)).label('VOLTAGE SPECS:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((7, -11.5)).label('CV OUT: 0-5V (5 octaves, C0-C5)', fontsize=8, halign='left')
d += elm.Label().at((7, -12)).label('TRIG OUT: 0-5V (V-Trig) or GND (S-Trig)', fontsize=8, halign='left')
d += elm.Label().at((7, -12.5)).label('CC OUT: 0-5V (CC 0-127 mapped)', fontsize=8, halign='left')
d += elm.Label().at((7, -13)).label('MCP4728: I2C address 0x60', fontsize=8, halign='left')
d += elm.Label().at((7, -13.5)).label('Reference: Internal 4.096V', fontsize=8, halign='left')

# Save schematic
d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_BOARD_FINAL.svg')
print("BOTTOM BOARD schematic saved to: BOTTOM_BOARD_FINAL.svg")
print("File size:", len(open('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_BOARD_FINAL.svg').read()), "bytes")
