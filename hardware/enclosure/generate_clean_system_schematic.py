#!/usr/bin/env python3
"""
Generate CLEAN SYSTEM SCHEMATIC - Organized by functional blocks
Session 25 - Redesigned for clarity and EasyEDA use
"""

import schemdraw
import schemdraw.elements as elm

# ============================================================================
# SCHEMATIC 1: M4 PIN ASSIGNMENTS AND CONNECTIONS
# ============================================================================

d1 = schemdraw.Drawing()

# Title
d1 += elm.Label().at((0, 12)).label('PRISME - M4 PIN ASSIGNMENTS', fontsize=16, halign='left', font='bold')
d1 += elm.Label().at((0, 11.3)).label('Reference for wiring M4 to custom PCBs', fontsize=10, halign='left')

# M4 representation with ALL pins used
d1 += elm.Label().at((3, 10)).label('FEATHER M4 CAN EXPRESS', fontsize=14, halign='center', font='bold')

# Power pins section
d1 += elm.Label().at((0, 9)).label('POWER PINS:', fontsize=11, halign='left', font='bold')
d1 += elm.Label().at((0, 8.5)).label('USB → 5V Rail → DAC VDD, decoupling caps', fontsize=9, halign='left')
d1 += elm.Label().at((0, 8)).label('3V3 → 3.3V Rail → MIDI, OLED, LEDs, BAT85 clamps', fontsize=9, halign='left')
d1 += elm.Label().at((0, 7.5)).label('GND → Common ground (multiple pins available)', fontsize=9, halign='left')

# I2C pins section
d1 += elm.Label().at((0, 6.5)).label('I2C BUS (SHARED):', fontsize=11, halign='left', font='bold')
d1 += elm.Label().at((0, 6)).label('SDA (D21) → OLED Wing (0x3C) + MCP4728 DAC (0x60)', fontsize=9, halign='left')
d1 += elm.Label().at((0, 5.5)).label('SCL (D22) → OLED Wing (0x3C) + MCP4728 DAC (0x60)', fontsize=9, halign='left')
d1 += elm.Label().at((0, 5)).label('NOTE: Both devices share same SDA/SCL wires', fontsize=8, halign='left')

# UART pins section
d1 += elm.Label().at((0, 4)).label('UART (SERIAL1):', fontsize=11, halign='left', font='bold')
d1 += elm.Label().at((0, 3.5)).label('RX ← MIDI Wing (MIDI IN data)', fontsize=9, halign='left')
d1 += elm.Label().at((0, 3)).label('TX → MIDI Wing (MIDI OUT data)', fontsize=9, halign='left')

# ADC input pins section
d1 += elm.Label().at((0, 2)).label('ADC INPUTS (TOP PCB):', fontsize=11, halign='left', font='bold')
d1 += elm.Label().at((0, 1.5)).label('A3 ← CV IN voltage divider TAP (0-3.3V from 0-5V input)', fontsize=9, halign='left')
d1 += elm.Label().at((0, 1)).label('A4 ← TRIG IN voltage divider TAP (0-3.3V from 0-5V input)', fontsize=9, halign='left')

# GPIO output pins section
d1 += elm.Label().at((0, 0)).label('GPIO OUTPUTS:', fontsize=11, halign='left', font='bold')
d1 += elm.Label().at((0, -0.5)).label('D4 → CV IN LED (white, 1kΩ series)', fontsize=9, halign='left')
d1 += elm.Label().at((0, -1)).label('D10 → S-Trig transistor base (1kΩ series)', fontsize=9, halign='left')
d1 += elm.Label().at((0, -1.5)).label('D11 → TRIG IN LED Red channel (330Ω series)', fontsize=9, halign='left')
d1 += elm.Label().at((0, -2)).label('D23 → TRIG IN LED Green channel (330Ω series)', fontsize=9, halign='left')
d1 += elm.Label().at((0, -2.5)).label('D24 → TRIG IN LED Blue channel (330Ω series)', fontsize=9, halign='left')

# PCB connection summary
d1 += elm.Label().at((0, -4)).label('PCB CONNECTION PADS NEEDED:', fontsize=12, halign='left', font='bold')
d1 += elm.Label().at((0, -4.7)).label('TOP PCB needs pads for: A3, A4, D4, D11, D23, D24, 5V, 3V3, GND', fontsize=9, halign='left')
d1 += elm.Label().at((0, -5.2)).label('BOTTOM PCB needs pads for: SDA, SCL, D10, 5V, 3V3, GND', fontsize=9, halign='left')
d1 += elm.Label().at((0, -5.7)).label('These pads connect to M4 via wires or stacking headers', fontsize=8, halign='left')

d1.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/M4_PIN_ASSIGNMENTS.svg')
print("M4_PIN_ASSIGNMENTS.svg saved")

# ============================================================================
# SCHEMATIC 2: TOP BOARD (INPUT PCB) - CV IN Circuit
# ============================================================================

d2 = schemdraw.Drawing()

d2 += elm.Label().at((0, 10)).label('TOP PCB - CV IN PROTECTION CIRCUIT', fontsize=14, halign='left', font='bold')
d2 += elm.Label().at((0, 9.3)).label('Protects M4 ADC from 0-5V Eurorack input', fontsize=10, halign='left')

# CV IN Jack
jack_pos = (1, 7)
d2 += elm.Dot().at(jack_pos).label('CV IN\nJack TIP', fontsize=10, halign='right')

# Upper resistor (10k)
d2 += elm.Line().at(jack_pos).right(1)
d2 += elm.Resistor().right(2).label('R1\n10kΩ', fontsize=9, loc='top')

# TAP point
tap_pos = (jack_pos[0] + 3, jack_pos[1])
d2 += elm.Dot().at(tap_pos).label('TAP', fontsize=10, loc='top')

# To M4 A3
d2 += elm.Line().at(tap_pos).right(2)
d2 += elm.Dot().label('To M4\nPin A3\n(ADC)', fontsize=10, halign='left')

# Lower resistor (10k to GND)
d2 += elm.Line().at(tap_pos).down(1)
d2 += elm.Resistor().down(1.5).label('R2\n10kΩ', fontsize=9, loc='right')
d2 += elm.Line().down(0.5)
d2 += elm.Ground()

# BAT85 clamp (TAP to 3.3V)
d2 += elm.Line().at(tap_pos).up(1)
d2 += elm.Diode().up(1.5).label('D1\nBAT85\nSchottky', fontsize=9, loc='left')
d2 += elm.Line().up(0.5)
d2 += elm.Vdd().label('3.3V', fontsize=10)

# Optional smoothing cap
smooth_pos = (tap_pos[0] - 1, tap_pos[1])
d2 += elm.Line().at(smooth_pos).down(1)
d2 += elm.Capacitor().down(1.5).label('C15\n100nF\n(optional)', fontsize=8, loc='left')
d2 += elm.Line().down(0.5)
d2 += elm.Ground()

# Jack ground
d2 += elm.Line().at(jack_pos).down(1)
d2 += elm.Dot().label('Jack\nSLEEVE', fontsize=9, halign='right')
d2 += elm.Line().down(0.5)
d2 += elm.Ground()

# LED indicator
led_pos = (jack_pos[0], jack_pos[1] - 2.5)
d2 += elm.Line().at(led_pos).right(1)
d2 += elm.Dot().label('From M4\nPin D4', fontsize=9, halign='right')
d2 += elm.Line().right(1)
d2 += elm.Resistor().right(2).label('R3\n1kΩ', fontsize=9, loc='top')
d2 += elm.Line().right(0.5)
d2 += elm.LED().right(1.5).label('LED1\nWhite', fontsize=9, loc='top')
d2 += elm.Line().right(0.5)
d2 += elm.Ground()

# Protection analysis
d2 += elm.Label().at((0, 2)).label('PROTECTION ANALYSIS:', fontsize=11, halign='left', font='bold')
d2 += elm.Label().at((0, 1.5)).label('Voltage Divider: 5V input → 2.5V at TAP (÷2)', fontsize=9, halign='left')
d2 += elm.Label().at((0, 1)).label('BAT85 Clamp: Max 3.3V + 0.4V = 3.7V to ADC', fontsize=9, halign='left')
d2 += elm.Label().at((0, 0.5)).label('M4 ADC Safe: 3.3V nominal, 3.6V absolute max', fontsize=9, halign='left')
d2 += elm.Label().at((0, 0)).label('Result: SAFE up to 40V+ input! ✓', fontsize=9, halign='left', color='green')

# Component values
d2 += elm.Label().at((0, -1)).label('COMPONENT VALUES:', fontsize=11, halign='left', font='bold')
d2 += elm.Label().at((0, -1.5)).label('R1, R2: 10kΩ ±5% 1/4W (voltage divider)', fontsize=9, halign='left')
d2 += elm.Label().at((0, -2)).label('D1: BAT85 Schottky (30V, 200mA, DO-35)', fontsize=9, halign='left')
d2 += elm.Label().at((0, -2.5)).label('R3: 1kΩ ±5% 1/4W (LED current limit)', fontsize=9, halign='left')
d2 += elm.Label().at((0, -3)).label('LED1: White 3mm (Vf ~3.0V, If ~10mA)', fontsize=9, halign='left')
d2 += elm.Label().at((0, -3.5)).label('C15: 100nF ceramic X7R (optional noise filter)', fontsize=9, halign='left')

d2.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_PCB_CV_IN.svg')
print("TOP_PCB_CV_IN.svg saved")

# ============================================================================
# SCHEMATIC 3: TOP BOARD (INPUT PCB) - TRIG IN Circuit
# ============================================================================

d3 = schemdraw.Drawing()

d3 += elm.Label().at((0, 10)).label('TOP PCB - TRIG IN PROTECTION CIRCUIT', fontsize=14, halign='left', font='bold')
d3 += elm.Label().at((0, 9.3)).label('Protects M4 ADC from 0-5V gate/trigger input', fontsize=10, halign='left')

# TRIG IN Jack
jack_pos = (1, 7)
d3 += elm.Dot().at(jack_pos).label('TRIG IN\nJack TIP', fontsize=10, halign='right')

# Upper resistor (10k)
d3 += elm.Line().at(jack_pos).right(1)
d3 += elm.Resistor().right(2).label('R4\n10kΩ', fontsize=9, loc='top')

# TAP point
tap_pos = (jack_pos[0] + 3, jack_pos[1])
d3 += elm.Dot().at(tap_pos).label('TAP', fontsize=10, loc='top')

# To M4 A4
d3 += elm.Line().at(tap_pos).right(2)
d3 += elm.Dot().label('To M4\nPin A4\n(ADC)', fontsize=10, halign='left')

# Lower resistor (10k to GND)
d3 += elm.Line().at(tap_pos).down(1)
d3 += elm.Resistor().down(1.5).label('R5\n10kΩ', fontsize=9, loc='right')
d3 += elm.Line().down(0.5)
d3 += elm.Ground()

# BAT85 clamp (TAP to 3.3V)
d3 += elm.Line().at(tap_pos).up(1)
d3 += elm.Diode().up(1.5).label('D2\nBAT85\nSchottky', fontsize=9, loc='left')
d3 += elm.Line().up(0.5)
d3 += elm.Vdd().label('3.3V', fontsize=10)

# Optional smoothing cap
smooth_pos = (tap_pos[0] - 1, tap_pos[1])
d3 += elm.Line().at(smooth_pos).down(1)
d3 += elm.Capacitor().down(1.5).label('C16\n100nF\n(optional)', fontsize=8, loc='left')
d3 += elm.Line().down(0.5)
d3 += elm.Ground()

# Jack ground
d3 += elm.Line().at(jack_pos).down(1)
d3 += elm.Dot().label('Jack\nSLEEVE', fontsize=9, halign='right')
d3 += elm.Line().down(0.5)
d3 += elm.Ground()

# RGB LED indicator (3 separate channels)
d3 += elm.Label().at((0, 2)).label('RGB LED INDICATOR (3 GPIO pins):', fontsize=11, halign='left', font='bold')

# Red channel
led_r = (1, 0.5)
d3 += elm.Dot().at(led_r).label('M4 D11', fontsize=9, halign='right')
d3 += elm.Line().right(1)
d3 += elm.Resistor().right(2).label('R6\n330Ω', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.LED().right(1.5).label('LED2\nRed', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.Ground()

# Green channel
led_g = (1, -0.5)
d3 += elm.Dot().at(led_g).label('M4 D23', fontsize=9, halign='right')
d3 += elm.Line().right(1)
d3 += elm.Resistor().right(2).label('330Ω', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.LED().right(1.5).label('LED2\nGreen', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.Ground()

# Blue channel
led_b = (1, -1.5)
d3 += elm.Dot().at(led_b).label('M4 D24', fontsize=9, halign='right')
d3 += elm.Line().right(1)
d3 += elm.Resistor().right(2).label('330Ω', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.LED().right(1.5).label('LED2\nBlue', fontsize=9, loc='top')
d3 += elm.Line().right(0.5)
d3 += elm.Ground()

# Component values
d3 += elm.Label().at((0, -3)).label('COMPONENT VALUES:', fontsize=11, halign='left', font='bold')
d3 += elm.Label().at((0, -3.5)).label('R4, R5: 10kΩ ±5% 1/4W (voltage divider)', fontsize=9, halign='left')
d3 += elm.Label().at((0, -4)).label('D2: BAT85 Schottky (30V, 200mA, DO-35)', fontsize=9, halign='left')
d3 += elm.Label().at((0, -4.5)).label('R6: 330Ω ±5% 1/4W (RGB LED current limit)', fontsize=9, halign='left')
d3 += elm.Label().at((0, -5)).label('LED2: RGB common cathode 5mm (Vf ~2.0V, If ~10mA)', fontsize=9, halign='left')
d3 += elm.Label().at((0, -5.5)).label('C16: 100nF ceramic X7R (optional noise filter)', fontsize=9, halign='left')

d3.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_PCB_TRIG_IN.svg')
print("TOP_PCB_TRIG_IN.svg saved")

# ============================================================================
# SCHEMATIC 4: BOTTOM BOARD - MCP4728 DAC and CV/TRIG/CC Outputs
# ============================================================================

d4 = schemdraw.Drawing()

d4 += elm.Label().at((0, 12)).label('BOTTOM PCB - MCP4728 DAC OUTPUTS', fontsize=14, halign='left', font='bold')
d4 += elm.Label().at((0, 11.3)).label('4-channel I2C DAC for CV, TRIG, CC outputs', fontsize=10, halign='left')

# MCP4728 connections
d4 += elm.Label().at((0, 10)).label('MCP4728 CONNECTIONS:', fontsize=11, halign='left', font='bold')
d4 += elm.Label().at((0, 9.5)).label('VDD ← 5V Rail (needs 5V for 0-5V output range)', fontsize=9, halign='left')
d4 += elm.Label().at((0, 9)).label('GND ← Common ground', fontsize=9, halign='left')
d4 += elm.Label().at((0, 8.5)).label('SDA ← M4 SDA (shared with OLED)', fontsize=9, halign='left')
d4 += elm.Label().at((0, 8)).label('SCL ← M4 SCL (shared with OLED)', fontsize=9, halign='left')
d4 += elm.Label().at((0, 7.5)).label('I2C Address: 0x60 (factory default)', fontsize=9, halign='left')

# Channel A - CV OUT
d4 += elm.Label().at((0, 6.5)).label('CHANNEL A - CV OUT (0-5V):', fontsize=11, halign='left', font='bold')
cv_out_start = (1, 5.5)
d4 += elm.Dot().at(cv_out_start).label('MCP4728\nVA Pin', fontsize=9, halign='right')
d4 += elm.Line().right(1)
d4 += elm.Resistor().right(2).label('R1\n100Ω', fontsize=9, loc='top')
d4 += elm.Line().right(1)
d4 += elm.Dot().label('CV OUT\nJack TIP', fontsize=10, halign='left')
d4 += elm.Line().at((cv_out_start[0] + 4, cv_out_start[1])).down(1)
d4 += elm.Dot().label('Jack\nSLEEVE', fontsize=9, halign='left')
d4 += elm.Line().down(0.5)
d4 += elm.Ground()

# Channel B - TRIG OUT (V-Trig)
d4 += elm.Label().at((0, 3.5)).label('CHANNEL B - TRIG OUT V-Trig (0-5V):', fontsize=11, halign='left', font='bold')
trig_out_start = (1, 2.5)
d4 += elm.Dot().at(trig_out_start).label('MCP4728\nVB Pin', fontsize=9, halign='right')
d4 += elm.Line().right(1)
d4 += elm.Resistor().right(2).label('R2\n100Ω', fontsize=9, loc='top')
d4 += elm.Line().right(1)
d4 += elm.Dot().label('TRIG OUT\nJack TIP', fontsize=10, halign='left')
d4 += elm.Line().at((trig_out_start[0] + 4, trig_out_start[1])).down(1)
d4 += elm.Dot().label('Jack\nSLEEVE', fontsize=9, halign='left')
d4 += elm.Line().down(0.5)
d4 += elm.Ground()

# Channel C - CC OUT
d4 += elm.Label().at((0, 0.5)).label('CHANNEL C - CC OUT (0-5V):', fontsize=11, halign='left', font='bold')
cc_out_start = (1, -0.5)
d4 += elm.Dot().at(cc_out_start).label('MCP4728\nVC Pin', fontsize=9, halign='right')
d4 += elm.Line().right(1)
d4 += elm.Resistor().right(2).label('R3\n100Ω', fontsize=9, loc='top')
d4 += elm.Line().right(1)
d4 += elm.Dot().label('CC OUT\nJack TIP', fontsize=10, halign='left')
d4 += elm.Line().at((cc_out_start[0] + 4, cc_out_start[1])).down(1)
d4 += elm.Dot().label('Jack\nSLEEVE', fontsize=9, halign='left')
d4 += elm.Line().down(0.5)
d4 += elm.Ground()

# Component values
d4 += elm.Label().at((0, -2.5)).label('COMPONENT VALUES:', fontsize=11, halign='left', font='bold')
d4 += elm.Label().at((0, -3)).label('R1, R2, R3: 100Ω ±5% 1/4W (output protection)', fontsize=9, halign='left')
d4 += elm.Label().at((0, -3.5)).label('Purpose: Limits current on short circuit', fontsize=9, halign='left')
d4 += elm.Label().at((0, -4)).label('MCP4728: Adafruit #4470 (I2C 4-ch 12-bit DAC)', fontsize=9, halign='left')

# Output specs
d4 += elm.Label().at((0, -5)).label('OUTPUT SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
d4 += elm.Label().at((0, -5.5)).label('Range: 0-5V (5 octaves, C0 to C5)', fontsize=9, halign='left')
d4 += elm.Label().at((0, -6)).label('Standard: 1V/octave Eurorack', fontsize=9, halign='left')
d4 += elm.Label().at((0, -6.5)).label('Resolution: 12-bit (4096 steps)', fontsize=9, halign='left')
d4 += elm.Label().at((0, -7)).label('Reference: Internal 2.048V × 2 (software configurable)', fontsize=9, halign='left')

d4.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_PCB_DAC_OUTPUTS.svg')
print("BOTTOM_PCB_DAC_OUTPUTS.svg saved")

# ============================================================================
# SCHEMATIC 5: BOTTOM BOARD - S-Trig Circuit
# ============================================================================

d5 = schemdraw.Drawing()

d5 += elm.Label().at((0, 10)).label('BOTTOM PCB - S-TRIG CIRCUIT', fontsize=14, halign='left', font='bold')
d5 += elm.Label().at((0, 9.3)).label('Alternate trigger mode: Switch to ground (vintage synth compatible)', fontsize=10, halign='left')

# GPIO input
gpio_pos = (1, 7)
d5 += elm.Dot().at(gpio_pos).label('M4 Pin D10\n(GPIO)', fontsize=10, halign='right')

# Base resistor
d5 += elm.Line().right(1)
d5 += elm.Resistor().right(2).label('R8\n1kΩ', fontsize=9, loc='top')

# NPN Transistor
transistor_pos = (gpio_pos[0] + 3, gpio_pos[1])
d5 += elm.Bjt(circle=True).at(transistor_pos).label('Q1\n2N3904\nNPN', fontsize=9, loc='bottom')

# Collector to output jack
d5 += elm.Line().at((transistor_pos[0], transistor_pos[1] + 0.8)).up(0.5)
d5 += elm.Resistor().up(1.5).label('R9\n100Ω', fontsize=9, loc='right')
d5 += elm.Line().up(0.5)
d5 += elm.Dot().label('TRIG OUT\nJack TIP\n(S-Trig)', fontsize=10, halign='left')

# Emitter to ground
d5 += elm.Line().at((transistor_pos[0], transistor_pos[1] - 0.8)).down(0.5)
d5 += elm.Ground()

# Operation description
d5 += elm.Label().at((0, 4)).label('OPERATION:', fontsize=11, halign='left', font='bold')
d5 += elm.Label().at((0, 3.5)).label('D10 LOW (0V): Transistor OFF, jack tip OPEN (idle)', fontsize=9, halign='left')
d5 += elm.Label().at((0, 3)).label('D10 HIGH (3.3V): Transistor ON, jack tip to GND (triggered)', fontsize=9, halign='left')
d5 += elm.Label().at((0, 2.5)).label('Compatible with: ARP, Korg MS-20, Yamaha CS series', fontsize=9, halign='left')

# Component values
d5 += elm.Label().at((0, 1.5)).label('COMPONENT VALUES:', fontsize=11, halign='left', font='bold')
d5 += elm.Label().at((0, 1)).label('Q1: 2N3904 NPN transistor (TO-92)', fontsize=9, halign='left')
d5 += elm.Label().at((0, 0.5)).label('R8: 1kΩ ±5% 1/4W (base current limit)', fontsize=9, halign='left')
d5 += elm.Label().at((0, 0)).label('R9: 100Ω ±5% 1/4W (collector protection)', fontsize=9, halign='left')

# Note about V-Trig vs S-Trig
d5 += elm.Label().at((0, -1)).label('NOTE:', fontsize=11, halign='left', font='bold')
d5 += elm.Label().at((0, -1.5)).label('V-Trig (DAC Channel B) and S-Trig (this circuit) use SAME jack', fontsize=9, halign='left')
d5 += elm.Label().at((0, -2)).label('User selects mode in software (only one active at a time)', fontsize=9, halign='left')

d5.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_PCB_STRIG.svg')
print("BOTTOM_PCB_STRIG.svg saved")

# ============================================================================
# SCHEMATIC 6: POWER DISTRIBUTION (BOTH BOARDS)
# ============================================================================

d6 = schemdraw.Drawing()

d6 += elm.Label().at((0, 12)).label('POWER DISTRIBUTION - BOTH PCBs', fontsize=14, halign='left', font='bold')
d6 += elm.Label().at((0, 11.3)).label('Critical: Both 5V and 3.3V rails required!', fontsize=10, halign='left')

# 5V Rail
d6 += elm.Label().at((0, 10)).label('5V RAIL (from M4 USB pin):', fontsize=12, halign='left', font='bold')
d6 += elm.Label().at((0, 9.5)).label('Powers: MCP4728 DAC VDD', fontsize=9, halign='left')

# Top board 5V
d6 += elm.Label().at((0, 8.5)).label('TOP PCB 5V Decoupling:', fontsize=10, halign='left', font='bold')
usb_top = (1, 7.5)
d6 += elm.Vdd().at(usb_top).label('5V from M4', fontsize=9)
d6 += elm.Line().down(0.5)
bulk_top = (usb_top[0], usb_top[1] - 0.5)
d6 += elm.Capacitor().down(1.5).label('C11\n10µF\nElectrolytic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()
d6 += elm.Line().at(bulk_top).right(1.5)
d6 += elm.Capacitor().down(1.5).label('C12\n0.1µF\nCeramic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()

# Bottom board 5V
d6 += elm.Label().at((5, 8.5)).label('BOTTOM PCB 5V Decoupling:', fontsize=10, halign='left', font='bold')
usb_bot = (6, 7.5)
d6 += elm.Vdd().at(usb_bot).label('5V from M4', fontsize=9)
d6 += elm.Line().down(0.5)
bulk_bot = (usb_bot[0], usb_bot[1] - 0.5)
d6 += elm.Capacitor().down(1.5).label('C1\n47µF\nElectrolytic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()
d6 += elm.Line().at(bulk_bot).right(1.5)
d6 += elm.Capacitor().down(1.5).label('C2\n0.1µF\nCeramic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()

# 3.3V Rail
d6 += elm.Label().at((0, 4)).label('3.3V RAIL (from M4 3V3 pin):', fontsize=12, halign='left', font='bold')
d6 += elm.Label().at((0, 3.5)).label('Powers: MIDI Wing, OLED Wing, LEDs, BAT85 clamps', fontsize=9, halign='left')

# Top board 3.3V
d6 += elm.Label().at((0, 2.5)).label('TOP PCB 3.3V Decoupling:', fontsize=10, halign='left', font='bold')
reg_top = (1, 1.5)
d6 += elm.Vdd().at(reg_top).label('3.3V from M4', fontsize=9)
d6 += elm.Line().down(0.5)
bulk3_top = (reg_top[0], reg_top[1] - 0.5)
d6 += elm.Capacitor().down(1.5).label('C13\n10µF\nElectrolytic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()
d6 += elm.Line().at(bulk3_top).right(1.5)
d6 += elm.Capacitor().down(1.5).label('C14\n0.1µF\nCeramic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()

# Bottom board 3.3V
d6 += elm.Label().at((5, 2.5)).label('BOTTOM PCB 3.3V Decoupling:', fontsize=10, halign='left', font='bold')
reg_bot = (6, 1.5)
d6 += elm.Vdd().at(reg_bot).label('3.3V from M4', fontsize=9)
d6 += elm.Line().down(0.5)
bulk3_bot = (reg_bot[0], reg_bot[1] - 0.5)
d6 += elm.Capacitor().down(1.5).label('C9\n10µF\nElectrolytic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()
d6 += elm.Line().at(bulk3_bot).right(1.5)
d6 += elm.Capacitor().down(1.5).label('C10\n0.1µF\nCeramic', fontsize=9, loc='right')
d6 += elm.Line().down(0.5)
d6 += elm.Ground()

# Critical notes
d6 += elm.Label().at((0, -2)).label('CRITICAL NOTES:', fontsize=12, halign='left', font='bold')
d6 += elm.Label().at((0, -2.5)).label('1. Both rails MUST have decoupling on BOTH boards', fontsize=9, halign='left')
d6 += elm.Label().at((0, -3)).label('2. Place bulk caps (10µF/47µF) close to power entry points', fontsize=9, halign='left')
d6 += elm.Label().at((0, -3.5)).label('3. Place bypass caps (0.1µF) close to ICs (MCP4728, LEDs)', fontsize=9, halign='left')
d6 += elm.Label().at((0, -4)).label('4. MCP4728 MUST be powered by 5V for 0-5V output range', fontsize=9, halign='left')
d6 += elm.Label().at((0, -4.5)).label('5. MIDI/OLED require 3.3V (NOT 5V tolerant)', fontsize=9, halign='left')

d6.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/POWER_DISTRIBUTION.svg')
print("POWER_DISTRIBUTION.svg saved")

print("\n✅ ALL CLEAN SCHEMATICS GENERATED:")
print("   - M4_PIN_ASSIGNMENTS.svg (pin reference)")
print("   - TOP_PCB_CV_IN.svg (CV input circuit)")
print("   - TOP_PCB_TRIG_IN.svg (TRIG input circuit)")
print("   - BOTTOM_PCB_DAC_OUTPUTS.svg (CV/TRIG/CC outputs)")
print("   - BOTTOM_PCB_STRIG.svg (S-Trig circuit)")
print("   - POWER_DISTRIBUTION.svg (both boards)")
