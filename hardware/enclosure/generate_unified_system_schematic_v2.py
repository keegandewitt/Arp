#!/usr/bin/env python3
"""
Generate Unified System Schematic - Version 2

Session 27 (2025-11-04): Coordinate-planned approach
Shows complete system with ALL 7 LEDs included
Using absolute .at(x, y) positioning instead of relative .right()/.down()
"""

import schemdraw
import schemdraw.elements as elm

# Create drawing with plenty of space
d = schemdraw.Drawing(fontsize=9, font='sans-serif')

# ============================================================================
# TITLE SECTION
# ============================================================================
d += elm.Label().at((0, 19)).label('PRISME - UNIFIED SYSTEM SCHEMATIC', fontsize=14, font='bold', halign='left')
d += elm.Label().at((0, 18)).label('Complete Hardware Interconnection Diagram', fontsize=10, halign='left')
d += elm.Label().at((0, 17)).label('Session 27: USB-only power, all 7 LEDs shown', fontsize=9, halign='left')

# ============================================================================
# POWER SYSTEM (Left side)
# ============================================================================
d += elm.Label().at((0, 15.5)).label('USB-C POWER', fontsize=10, font='bold', halign='left')
d += elm.Gap().at((0, 15)).to((0, 14.5)).label('+', loc='left', fontsize=8)
d += elm.Line().at((0, 15)).to((2, 15)).label('5V', loc='top', fontsize=8)
d += elm.Dot().at((2, 15))
d += elm.Gap().at((0, 14.5)).to((0, 14)).label('−', loc='left', fontsize=8)
d += elm.Ground().at((0, 14))

# ============================================================================
# FEATHER M4 BLOCK (Center)
# ============================================================================
d += elm.Label().at((7.5, 16)).label('FEATHER M4 CAN EXPRESS', fontsize=11, font='bold', halign='center')

# Draw M4 box manually
d += elm.Line().at((5, 15)).to((10, 15))
d += elm.Line().at((10, 15)).to((10, 6))
d += elm.Line().at((10, 6)).to((5, 6))
d += elm.Line().at((5, 6)).to((5, 15))

# Pin labels inside box
d += elm.Label().at((7.5, 14)).label('Power:', fontsize=9, halign='center')
d += elm.Label().at((7.5, 13.5)).label('USB (5V), 3V3 (3.3V), GND', fontsize=8, halign='center')
d += elm.Label().at((7.5, 12.5)).label('I2C:', fontsize=9, halign='center')
d += elm.Label().at((7.5, 12)).label('SDA/SCL → OLED + MCP4728', fontsize=8, halign='center')
d += elm.Label().at((7.5, 11)).label('UART:', fontsize=9, halign='center')
d += elm.Label().at((7.5, 10.5)).label('RX/TX → MIDI FeatherWing', fontsize=8, halign='center')
d += elm.Label().at((7.5, 9.5)).label('ADC Inputs:', fontsize=9, halign='center')
d += elm.Label().at((7.5, 9)).label('A3 ← CV IN, A4 ← TRIG IN', fontsize=8, halign='center')
d += elm.Label().at((7.5, 8)).label('GPIO Outputs (LEDs):', fontsize=9, halign='center')
d += elm.Label().at((7.5, 7.5)).label('D4, D11/D23/D24, D12, A0/A1/A2,', fontsize=7, halign='center')
d += elm.Label().at((7.5, 7)).label('D25, CAN_TX, A5', fontsize=7, halign='center')

# Power connections to M4
d += elm.Line().at((2, 15)).to((5, 15))
d += elm.Label().at((3.5, 15.3)).label('5V', fontsize=8, halign='center')
d += elm.Line().at((2, 14)).to((5, 14))
d += elm.Label().at((3.5, 14.3)).label('GND', fontsize=8, halign='center')

# ============================================================================
# INPUT CIRCUITS - TOP PCB (Right upper section)
# ============================================================================
d += elm.Label().at((11, 11)).label('INPUT CIRCUITS (TOP PCB)', fontsize=10, font='bold', halign='left')

# CV IN circuit
d += elm.Label().at((11, 10.5)).label('CV IN:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, 10)).to((12, 10))
d += elm.Label().at((11.5, 10.2)).label('R1 10kΩ', fontsize=7, halign='center')
d += elm.Dot().at((12, 10)).label('TAP', loc='top', fontsize=7)
d += elm.Resistor().at((12, 10)).down(0.8).label('R2\n10kΩ', fontsize=7, loc='right')
d += elm.Ground()
d += elm.Line().at((12, 10)).to((13, 10))
d += elm.Label().at((12.5, 10.2)).label('→ A3', fontsize=7, halign='center')
d += elm.Line().at((13, 10)).to((13.5, 10))
d += elm.Resistor().at((13.5, 10)).right(0.8).label('1kΩ', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('White', fontsize=7, loc='top')
d += elm.Label().at((15, 10)).label('D4', fontsize=7, halign='left')

# TRIG IN circuit
d += elm.Label().at((11, 8.5)).label('TRIG IN:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, 8)).to((12, 8))
d += elm.Label().at((11.5, 8.2)).label('R4 10kΩ', fontsize=7, halign='center')
d += elm.Dot().at((12, 8)).label('TAP', loc='top', fontsize=7)
d += elm.Resistor().at((12, 8)).down(0.8).label('R5\n10kΩ', fontsize=7, loc='right')
d += elm.Ground()
d += elm.Line().at((12, 8)).to((13, 8))
d += elm.Label().at((12.5, 8.2)).label('→ A4', fontsize=7, halign='center')
d += elm.Line().at((13, 8)).to((13.5, 8))
d += elm.Resistor().at((13.5, 8)).right(0.8).label('330Ω', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('RGB', fontsize=7, loc='top')
d += elm.Label().at((15, 8)).label('D11/D23/D24', fontsize=6, halign='left')
d += elm.Label().at((15, 7.7)).label('(R/G/B)', fontsize=6, halign='left')

# ============================================================================
# OUTPUT CIRCUITS - BOTTOM PCB (Right lower section)
# ============================================================================
d += elm.Label().at((11, 5.5)).label('OUTPUT CIRCUITS (BOTTOM PCB)', fontsize=10, font='bold', halign='left')

# CV OUT circuit
d += elm.Label().at((11, 5)).label('CV OUT:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, 4.7)).to((12, 4.7))
d += elm.Label().at((11.5, 4.9)).label('MCP4728 Ch A', fontsize=7, halign='center')
d += elm.Resistor().at((12, 4.7)).right(0.8).label('100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Label().at((13.8, 4.9)).label('Jack', fontsize=7, halign='center')
d += elm.Line().at((14, 4.7)).to((14.5, 4.7))
d += elm.Resistor().at((14.5, 4.7)).right(0.8).label('1kΩ', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('White', fontsize=7, loc='top')
d += elm.Label().at((16.5, 4.7)).label('D12', fontsize=7, halign='left')

# TRIG OUT circuit (V-Trig + S-Trig)
d += elm.Label().at((11, 3.5)).label('TRIG OUT:', fontsize=9, font='bold', halign='left')
d += elm.Label().at((11.5, 3.2)).label('Ch C (V-Trig)', fontsize=7, halign='left')
d += elm.Label().at((11.5, 2.9)).label('D10 (S-Trig)', fontsize=7, halign='left')
d += elm.Line().at((13, 3.5)).to((13.5, 3.5))
d += elm.Label().at((13.5, 3.7)).label('Jack', fontsize=7, halign='center')
d += elm.Line().at((14, 3.5)).to((14.5, 3.5))
d += elm.Resistor().at((14.5, 3.5)).right(0.8).label('330Ω', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('RGB', fontsize=7, loc='top')
d += elm.Label().at((16.5, 3.5)).label('A0/A1/A2', fontsize=6, halign='left')
d += elm.Label().at((16.5, 3.2)).label('(R/G/B)', fontsize=6, halign='left')

# CC OUT circuit
d += elm.Label().at((11, 2)).label('CC OUT:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, 1.7)).to((12, 1.7))
d += elm.Label().at((11.5, 1.9)).label('MCP4728 Ch D', fontsize=7, halign='center')
d += elm.Resistor().at((12, 1.7)).right(0.8).label('100Ω', fontsize=7, loc='top')
d += elm.Line().right(0.5)
d += elm.Label().at((13.8, 1.9)).label('Jack', fontsize=7, halign='center')
d += elm.Line().at((14, 1.7)).to((14.5, 1.7))
d += elm.Resistor().at((14.5, 1.7)).right(0.8).label('1kΩ', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('White', fontsize=7, loc='top')
d += elm.Label().at((16.5, 1.7)).label('D25', fontsize=7, halign='left')

# ============================================================================
# MIDI CIRCUITS (Bottom right)
# ============================================================================
d += elm.Label().at((11, 0.5)).label('MIDI (BREADBOARD)', fontsize=10, font='bold', halign='left')

# MIDI OUT
d += elm.Label().at((11, 0)).label('MIDI OUT:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, -0.3)).to((12, -0.3))
d += elm.Label().at((11.5, -0.1)).label('TX → FeatherWing', fontsize=7, halign='center')
d += elm.Line().at((12.5, -0.3)).to((13, -0.3))
d += elm.Label().at((13, -0.1)).label('DIN Jack', fontsize=7, halign='center')
d += elm.Line().at((13.5, -0.3)).to((14, -0.3))
d += elm.Resistor().at((14, -0.3)).right(0.8).label('1kΩ', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('White', fontsize=7, loc='top')
d += elm.Label().at((16, -0.3)).label('CAN_TX', fontsize=7, halign='left')

# MIDI IN
d += elm.Label().at((11, -1.3)).label('MIDI IN:', fontsize=9, font='bold', halign='left')
d += elm.Line().at((11, -1.6)).to((12, -1.6))
d += elm.Label().at((11.5, -1.4)).label('RX ← FeatherWing', fontsize=7, halign='center')
d += elm.Line().at((12.5, -1.6)).to((13, -1.6))
d += elm.Label().at((13, -1.4)).label('DIN Jack', fontsize=7, halign='center')
d += elm.Line().at((13.5, -1.6)).to((14, -1.6))
d += elm.Resistor().at((14, -1.6)).right(0.8).label('1kΩ', fontsize=7, loc='top')
d += elm.LED().right(0.5).label('White', fontsize=7, loc='top')
d += elm.Label().at((16, -1.6)).label('A5', fontsize=7, halign='left')

# ============================================================================
# COMPONENT SUMMARY TABLE
# ============================================================================
d += elm.Label().at((0, -3)).label('COMPONENT VALUES:', fontsize=10, font='bold', halign='left')
d += elm.Label().at((0, -3.5)).label('Resistors: 10kΩ (voltage dividers), 100Ω (DAC output protection)', fontsize=8, halign='left')
d += elm.Label().at((0, -4)).label('          1kΩ (white LED current limit), 330Ω (RGB LED current limit)', fontsize=8, halign='left')
d += elm.Label().at((0, -4.5)).label('Diodes: BAT85 Schottky (30V 200mA, input clamps - see individual schematics)', fontsize=8, halign='left')
d += elm.Label().at((0, -5)).label('LEDs: 5× white 3mm, 2× RGB 5mm common cathode', fontsize=8, halign='left')
d += elm.Label().at((0, -5.5)).label('DAC: MCP4728 4-channel 12-bit I2C (address 0x60)', fontsize=8, halign='left')

# ============================================================================
# LED SUMMARY
# ============================================================================
d += elm.Label().at((0, -6.5)).label('ALL 7 LED INDICATORS:', fontsize=10, font='bold', halign='left')
d += elm.Label().at((0, -7)).label('Inputs:  D4 (CV IN white), D11/D23/D24 (TRIG IN RGB)', fontsize=8, halign='left')
d += elm.Label().at((0, -7.5)).label('Outputs: D12 (CV OUT white), A0/A1/A2 (TRIG OUT RGB), D25 (CC OUT white)', fontsize=8, halign='left')
d += elm.Label().at((0, -8)).label('MIDI:    CAN_TX (MIDI OUT white), A5 (MIDI IN white)', fontsize=8, halign='left')

# ============================================================================
# NOTES
# ============================================================================
d += elm.Label().at((0, -9)).label('NOTES:', fontsize=10, font='bold', halign='left')
d += elm.Label().at((0, -9.5)).label('• Power: USB-C only (no battery) - see POWER_DISTRIBUTION.svg', fontsize=8, halign='left')
d += elm.Label().at((0, -10)).label('• Input protection: BAT85 diodes + voltage dividers - see TOP_PCB_*.svg', fontsize=8, halign='left')
d += elm.Label().at((0, -10.5)).label('• OLED FeatherWing: Stacked on M4 (I2C 0x3C, buttons D5/D6/D9)', fontsize=8, halign='left')
d += elm.Label().at((0, -11)).label('• MIDI FeatherWing: On breadboard (not stacked)', fontsize=8, halign='left')

# Save
d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC_V2.svg')
print("✅ Generated: UNIFIED_SYSTEM_SCHEMATIC_V2.svg (coordinate-planned, all 7 LEDs)")
