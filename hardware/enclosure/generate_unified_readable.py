#!/usr/bin/env python3
"""
Generate READABLE UNIFIED SYSTEM SCHEMATIC
Session 25 - Redesigned with intelligent spacing and clear layout
"""

import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()

# Title
d += elm.Label().at((0, 32)).label('PRISME - COMPLETE HARDWARE SCHEMATIC', fontsize=18, halign='left', font='bold')
d += elm.Label().at((0, 31)).label('Unified system diagram with all interconnections', fontsize=12, halign='left')

# ============================================================================
# SECTION 1: POWER INPUT AND DISTRIBUTION (TOP)
# ============================================================================

d += elm.Label().at((0, 28)).label('POWER INPUT', fontsize=14, halign='left', font='bold')

# USB-C Input
usb_x = 2
usb_y = 27
d += elm.Dot().at((usb_x, usb_y)).label('USB-C\n5V IN', fontsize=10, halign='right')
d += elm.Line().right(2)
usb_node = (usb_x + 2, usb_y)
d += elm.Dot().at(usb_node)
d += elm.Vdd().at((usb_node[0], usb_node[1] + 0.8)).label('5V RAIL', fontsize=11)

# 5V distribution
d += elm.Label().at((usb_node[0] + 1, usb_y + 0.8)).label('→ M4 USB pin', fontsize=9, halign='left')
d += elm.Label().at((usb_node[0] + 1, usb_y + 0.3)).label('→ DAC VDD (bottom board)', fontsize=9, halign='left')
d += elm.Label().at((usb_node[0] + 1, usb_y - 0.2)).label('→ Top board decoupling', fontsize=9, halign='left')

# 3.3V rail (from M4 regulator)
reg_x = 12
reg_y = 27
d += elm.Dot().at((reg_x, reg_y)).label('M4 3V3\nRegulator', fontsize=10, halign='right')
d += elm.Line().right(2)
reg_node = (reg_x + 2, reg_y)
d += elm.Dot().at(reg_node)
d += elm.Vdd().at((reg_node[0], reg_node[1] + 0.8)).label('3.3V RAIL', fontsize=11)

# 3.3V distribution
d += elm.Label().at((reg_node[0] + 1, reg_y + 0.8)).label('→ OLED Wing', fontsize=9, halign='left')
d += elm.Label().at((reg_node[0] + 1, reg_y + 0.3)).label('→ MIDI Wing', fontsize=9, halign='left')
d += elm.Label().at((reg_node[0] + 1, reg_y - 0.2)).label('→ LEDs, BAT85 clamps', fontsize=9, halign='left')
d += elm.Label().at((reg_node[0] + 1, reg_y - 0.7)).label('→ Both board decoupling', fontsize=9, halign='left')

# Ground
d += elm.Ground().at((8, 26)).label('COMMON GROUND', fontsize=11, halign='left')

# ============================================================================
# SECTION 2: FEATHER M4 AT CENTER
# ============================================================================

m4_x = 10
m4_y = 18

d += elm.Label().at((m4_x - 4, m4_y + 5)).label('FEATHER M4 CAN EXPRESS - ATSAMD51', fontsize=14, halign='center', font='bold')

# Draw M4 as large clear IC
d += elm.Ic(pins=[
    # Left side - Power
    elm.IcPin(name='USB (5V)', side='left', pin='1'),
    elm.IcPin(name='GND', side='left', pin='2'),
    elm.IcPin(name='3V3', side='left', pin='3'),
    # Left side - I2C
    elm.IcPin(name='SDA', side='left', pin='4'),
    elm.IcPin(name='SCL', side='left', pin='5'),
    # Bottom - ADC
    elm.IcPin(name='A3 (ADC)', side='bot', pin='6'),
    elm.IcPin(name='A4 (ADC)', side='bot', pin='7'),
    # Top - UART
    elm.IcPin(name='RX (UART)', side='top', pin='8'),
    elm.IcPin(name='TX (UART)', side='top', pin='9'),
    # Right - GPIO
    elm.IcPin(name='D4', side='right', pin='10'),
    elm.IcPin(name='D10', side='right', pin='11'),
    elm.IcPin(name='D11', side='right', pin='12'),
    elm.IcPin(name='D23', side='right', pin='13'),
    elm.IcPin(name='D24', side='right', pin='14'),
]).at((m4_x, m4_y)).label('M4\nCortex-M4\n120MHz', fontsize=10, loc='center')

# ============================================================================
# SECTION 3: I2C BUS (LEFT SIDE - VERTICAL BUS)
# ============================================================================

d += elm.Label().at((0, 20)).label('I2C BUS (SHARED)', fontsize=14, halign='left', font='bold')

# SDA bus line (vertical)
sda_x = 3
sda_top = 22
sda_bot = 10
d += elm.Line().at((sda_x, sda_top)).down(sda_top - sda_bot)
d += elm.Label().at((sda_x - 0.5, (sda_top + sda_bot) / 2)).label('SDA', fontsize=10, halign='right')

# SCL bus line (vertical, parallel to SDA)
scl_x = 4
d += elm.Line().at((scl_x, sda_top)).down(sda_top - sda_bot)
d += elm.Label().at((scl_x + 0.5, (sda_top + sda_bot) / 2)).label('SCL', fontsize=10, halign='left')

# Connect M4 to I2C bus
m4_sda_pin = (m4_x - 4, m4_y + 2.8)
d += elm.Line().at(m4_sda_pin).left(m4_x - 4 - sda_x)
d += elm.Dot().at((sda_x, m4_y + 2.8))

m4_scl_pin = (m4_x - 4, m4_y + 2.1)
d += elm.Line().at(m4_scl_pin).left(m4_x - 4 - scl_x)
d += elm.Dot().at((scl_x, m4_y + 2.1))

# OLED connection to I2C bus
oled_y = 20
d += elm.Dot().at((sda_x, oled_y))
d += elm.Line().right(1)
d += elm.Dot().at((scl_x, oled_y))
d += elm.Line().right(0.5)
d += elm.Label().at((scl_x + 2.5, oled_y)).label('OLED Wing (0x3C)', fontsize=11, halign='left', font='bold')
d += elm.Label().at((scl_x + 2.5, oled_y - 0.6)).label('128×64 Display, 3.3V', fontsize=9, halign='left')

# DAC connection to I2C bus
dac_i2c_y = 12
d += elm.Dot().at((sda_x, dac_i2c_y))
d += elm.Line().right(1)
d += elm.Dot().at((scl_x, dac_i2c_y))
d += elm.Line().right(0.5)
d += elm.Label().at((scl_x + 2.5, dac_i2c_y)).label('MCP4728 DAC (0x60)', fontsize=11, halign='left', font='bold')
d += elm.Label().at((scl_x + 2.5, dac_i2c_y - 0.6)).label('4-ch 12-bit, 5V power', fontsize=9, halign='left')

# ============================================================================
# SECTION 4: UART - MIDI (TOP)
# ============================================================================

d += elm.Label().at((m4_x - 2, 24)).label('MIDI I/O (UART)', fontsize=14, halign='center', font='bold')

# RX line
m4_rx_pin = (m4_x - 4, m4_y + 4)
d += elm.Line().at(m4_rx_pin).up(2)
d += elm.Dot().at((m4_rx_pin[0], m4_rx_pin[1] + 2))
d += elm.Line().right(2)
d += elm.Label().at((m4_rx_pin[0] + 3, m4_rx_pin[1] + 2)).label('MIDI IN (DIN-5)', fontsize=10, halign='left')

# TX line
m4_tx_pin = (m4_x - 4, m4_y + 4.7)
d += elm.Line().at(m4_tx_pin).up(1.3)
d += elm.Dot().at((m4_tx_pin[0], m4_tx_pin[1] + 1.3))
d += elm.Line().right(2)
d += elm.Label().at((m4_tx_pin[0] + 3, m4_tx_pin[1] + 1.3)).label('MIDI OUT (DIN-5)', fontsize=10, halign='left')

d += elm.Label().at((m4_x, 23)).label('MIDI FeatherWing', fontsize=11, halign='center')
d += elm.Label().at((m4_x, 22.4)).label('3.3V power', fontsize=9, halign='center')

# ============================================================================
# SECTION 5: CV IN CIRCUIT (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((0, 8)).label('CV IN - TOP BOARD', fontsize=14, halign='left', font='bold')

cv_jack_x = 1
cv_jack_y = 6

# Jack
d += elm.Dot().at((cv_jack_x, cv_jack_y)).label('CV IN\nJack TIP', fontsize=10, halign='right')

# Voltage divider - upper resistor
d += elm.Line().right(1.5)
d += elm.Resistor().right(3).label('R1 = 10kΩ', fontsize=10, loc='top')

# TAP point
cv_tap_x = cv_jack_x + 4.5
cv_tap_y = cv_jack_y
d += elm.Dot().at((cv_tap_x, cv_tap_y))
d += elm.Label().at((cv_tap_x, cv_tap_y + 0.5)).label('TAP', fontsize=10, halign='center')

# Lower resistor to ground
d += elm.Line().at((cv_tap_x, cv_tap_y)).down(1.5)
d += elm.Resistor().down(2).label('R2 = 10kΩ', fontsize=10, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp to 3.3V
d += elm.Line().at((cv_tap_x, cv_tap_y)).up(1.5)
d += elm.Diode().up(2).label('D1 = BAT85\nSchottky', fontsize=10, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=10)

# Connection to M4 A3
d += elm.Line().at((cv_tap_x, cv_tap_y)).right(2)
cv_to_m4_node = (cv_tap_x + 2, cv_tap_y)
d += elm.Dot().at(cv_to_m4_node)
d += elm.Line().up(m4_y - 2 - cv_tap_y)
d += elm.Line().right(m4_x - 4 - cv_to_m4_node[0])

# Jack ground
d += elm.Line().at((cv_jack_x, cv_jack_y)).down(1)
d += elm.Ground()

# CV LED indicator
cv_led_y = 3.5
d += elm.Dot().at((cv_jack_x, cv_led_y)).label('M4 D4 →', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Resistor().right(2.5).label('R3 = 1kΩ', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.LED().right(2).label('White LED', fontsize=9, loc='top')
d += elm.Line().right(0.5)
d += elm.Ground()

# ============================================================================
# SECTION 6: TRIG IN CIRCUIT (BOTTOM LEFT)
# ============================================================================

d += elm.Label().at((0, 0)).label('TRIG IN - TOP BOARD', fontsize=14, halign='left', font='bold')

trig_jack_x = 1
trig_jack_y = -2

# Jack
d += elm.Dot().at((trig_jack_x, trig_jack_y)).label('TRIG IN\nJack TIP', fontsize=10, halign='right')

# Voltage divider - upper resistor
d += elm.Line().right(1.5)
d += elm.Resistor().right(3).label('R4 = 10kΩ', fontsize=10, loc='top')

# TAP point
trig_tap_x = trig_jack_x + 4.5
trig_tap_y = trig_jack_y
d += elm.Dot().at((trig_tap_x, trig_tap_y))
d += elm.Label().at((trig_tap_x, trig_tap_y + 0.5)).label('TAP', fontsize=10, halign='center')

# Lower resistor to ground
d += elm.Line().at((trig_tap_x, trig_tap_y)).down(1.5)
d += elm.Resistor().down(2).label('R5 = 10kΩ', fontsize=10, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# BAT85 clamp to 3.3V
d += elm.Line().at((trig_tap_x, trig_tap_y)).up(1.5)
d += elm.Diode().up(2).label('D2 = BAT85\nSchottky', fontsize=10, loc='left')
d += elm.Line().up(0.5)
d += elm.Vdd().label('3.3V', fontsize=10)

# Connection to M4 A4
d += elm.Line().at((trig_tap_x, trig_tap_y)).right(2)
trig_to_m4_node = (trig_tap_x + 2, trig_tap_y)
d += elm.Dot().at(trig_to_m4_node)
d += elm.Line().up(m4_y - 2 - 0.7 - trig_tap_y)
d += elm.Line().right(m4_x - 4 - trig_to_m4_node[0])

# Jack ground
d += elm.Line().at((trig_jack_x, trig_jack_y)).down(1)
d += elm.Ground()

# TRIG RGB LED
trig_led_y = -5
d += elm.Label().at((trig_jack_x, trig_led_y)).label('M4 GPIO →', fontsize=9, halign='right')
d += elm.Label().at((trig_jack_x + 1.5, trig_led_y + 0.5)).label('D11 (R)', fontsize=8, halign='center')
d += elm.Line().at((trig_jack_x + 1.5, trig_led_y)).down(0.3)
d += elm.Resistor().down(1.2).label('330Ω', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.LED().down(1).label('R', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

d += elm.Label().at((trig_jack_x + 3.5, trig_led_y + 0.5)).label('D23 (G)', fontsize=8, halign='center')
d += elm.Line().at((trig_jack_x + 3.5, trig_led_y)).down(0.3)
d += elm.Resistor().down(1.2).label('330Ω', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.LED().down(1).label('G', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

d += elm.Label().at((trig_jack_x + 5.5, trig_led_y + 0.5)).label('D24 (B)', fontsize=8, halign='center')
d += elm.Line().at((trig_jack_x + 5.5, trig_led_y)).down(0.3)
d += elm.Resistor().down(1.2).label('330Ω', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.LED().down(1).label('B', fontsize=8, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 7: DAC OUTPUTS (RIGHT SIDE)
# ============================================================================

d += elm.Label().at((16, 8)).label('DAC OUTPUTS - BOTTOM BOARD', fontsize=14, halign='left', font='bold')

dac_out_x = 17

# Channel A - CV OUT
cv_out_y = 6
d += elm.Dot().at((dac_out_x, cv_out_y)).label('DAC CH A\n(VA pin)', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Resistor().right(3).label('R1 = 100Ω', fontsize=10, loc='top')
d += elm.Line().right(1)
d += elm.Dot().label('CV OUT\nJack TIP', fontsize=10, halign='left')
d += elm.Line().at((dac_out_x + 5, cv_out_y)).down(1)
d += elm.Ground()

# Channel B - TRIG OUT (V-Trig)
trig_v_out_y = 3.5
d += elm.Dot().at((dac_out_x, trig_v_out_y)).label('DAC CH B\n(VB pin)', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Resistor().right(3).label('R2 = 100Ω', fontsize=10, loc='top')
d += elm.Line().right(1)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(V-Trig)', fontsize=9, halign='left')
d += elm.Line().at((dac_out_x + 5, trig_v_out_y)).down(1)
d += elm.Ground()

# Channel C - CC OUT
cc_out_y = 1
d += elm.Dot().at((dac_out_x, cc_out_y)).label('DAC CH C\n(VC pin)', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Resistor().right(3).label('R3 = 100Ω', fontsize=10, loc='top')
d += elm.Line().right(1)
d += elm.Dot().label('CC OUT\nJack TIP', fontsize=10, halign='left')
d += elm.Line().at((dac_out_x + 5, cc_out_y)).down(1)
d += elm.Ground()

d += elm.Label().at((dac_out_x + 2.5, -1)).label('All outputs: 0-5V, 1V/octave', fontsize=9, halign='center')

# ============================================================================
# SECTION 8: S-TRIG CIRCUIT (RIGHT BOTTOM)
# ============================================================================

d += elm.Label().at((16, -3)).label('S-TRIG - BOTTOM BOARD', fontsize=14, halign='left', font='bold')

strig_y = -5

# From M4 D10
d += elm.Dot().at((dac_out_x, strig_y)).label('M4 D10\nGPIO', fontsize=9, halign='right')
d += elm.Line().right(1)
d += elm.Resistor().right(3).label('R8 = 1kΩ', fontsize=10, loc='top')

# Transistor
q_x = dac_out_x + 4
d += elm.Bjt(circle=True).at((q_x, strig_y)).label('Q1 = 2N3904\nNPN', fontsize=9, loc='bottom')

# Collector to jack
d += elm.Line().at((q_x, strig_y + 1)).up(1)
d += elm.Resistor().up(2).label('R9 = 100Ω', fontsize=9, loc='right')
d += elm.Line().up(1)
d += elm.Dot().label('TRIG OUT\nJack TIP\n(S-Trig)', fontsize=9, halign='left')

# Emitter to ground
d += elm.Line().at((q_x, strig_y - 1)).down(1)
d += elm.Ground()

d += elm.Label().at((dac_out_x + 2, -8.5)).label('Switch to GND (vintage synths)', fontsize=9, halign='center')

# ============================================================================
# NOTES
# ============================================================================

d += elm.Label().at((0, -11)).label('NOTES:', fontsize=13, halign='left', font='bold')
d += elm.Label().at((0, -11.7)).label('1. I2C bus shared: OLED (0x3C) + DAC (0x60) on same SDA/SCL wires', fontsize=9, halign='left')
d += elm.Label().at((0, -12.3)).label('2. Input protection: 10kΩ voltage divider + BAT85 clamp = safe for 0-40V+ input', fontsize=9, halign='left')
d += elm.Label().at((0, -12.9)).label('3. Output protection: 100Ω series resistors on all DAC channels', fontsize=9, halign='left')
d += elm.Label().at((0, -13.5)).label('4. V-Trig and S-Trig share same TRIG OUT jack (software selectable)', fontsize=9, halign='left')
d += elm.Label().at((0, -14.1)).label('5. Power decoupling: Each rail needs bulk + bypass caps on both boards', fontsize=9, halign='left')
d += elm.Label().at((0, -14.7)).label('6. MCP4728 requires 5V power for 0-5V output range (NOT 3.3V)', fontsize=9, halign='left')

d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg')
print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg saved (READABLE VERSION)")
print("\n📐 Redesigned with intelligent spacing:")
print("   - Much larger component separation")
print("   - Clear signal flow left-to-right")
print("   - Vertical I2C bus on left")
print("   - Power at top")
print("   - Inputs on bottom left")
print("   - Outputs on bottom right")
print("   - M4 at center with all connections visible")
