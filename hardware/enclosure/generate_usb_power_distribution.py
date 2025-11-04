#!/usr/bin/env python3
"""
Generate USB-Only Power Distribution Schematic

Session 27 (2025-11-04): Simplified power system - removed battery and powerboost
Now: USB-C → M4 USB pin → 5V/3.3V rails
"""

import schemdraw
import schemdraw.elements as elm

# Create drawing
d = schemdraw.Drawing(fontsize=10, font='sans-serif')

# Title
d += elm.Label().at((0, 8)).label('PRISME Power Distribution - USB-Only', fontsize=14, font='bold', halign='left')
d += elm.Label().at((0, 7.5)).label('Session 27: Simplified (No Battery/Powerboost)', fontsize=10, halign='left')

# USB-C Connector (top left)
d += elm.Label().at((0, 6)).label('USB-C CONNECTOR', fontsize=11, font='bold', halign='left')
d += elm.Gap().at((0, 5.5)).to((0, 5)).label('+', loc='left', fontsize=8)
d += elm.Line().at((0, 5.5)).to((1.5, 5.5)).label('5V', loc='top', fontsize=9)
d += elm.Dot().at((1.5, 5.5))
d += elm.Gap().at((0, 5)).to((0, 4.5)).label('−', loc='left', fontsize=8)
d += elm.Line().at((0, 5)).to((1.5, 5)).label('GND', loc='bottom', fontsize=9)
d += elm.Ground().at((1.5, 5))

# Feather M4 block (center)
d += elm.Label().at((4, 6.5)).label('FEATHER M4 CAN EXPRESS', fontsize=11, font='bold', halign='center')

# USB pin input (5V)
d += elm.Line().at((1.5, 5.5)).to((3, 5.5))
d += elm.Dot().at((3, 5.5)).label('USB pin', loc='top', fontsize=8)

# M4 box (using lines instead of Rect to avoid coordinate issues)
d += elm.Line().at((3, 6)).to((5, 6))
d += elm.Line().at((5, 6)).to((5, 3))
d += elm.Line().at((5, 3)).to((3, 3))
d += elm.Line().at((3, 3)).to((3, 6))
d += elm.Label().at((4, 5.5)).label('M4', fontsize=9, halign='center')
d += elm.Label().at((4, 5)).label('USB → 5V', fontsize=8, halign='center')
d += elm.Label().at((4, 4.5)).label('3V3 ← Regulator', fontsize=8, halign='center')
d += elm.Label().at((4, 4)).label('(500mA)', fontsize=7, halign='center')

# 5V Rail output (right side, top)
d += elm.Line().at((5, 5.5)).to((7, 5.5))
d += elm.Dot().at((7, 5.5))
d += elm.Label().at((7.2, 5.5)).label('5V RAIL', fontsize=10, font='bold', halign='left')

# 3.3V Rail output (right side, bottom)
d += elm.Line().at((5, 4)).to((7, 4))
d += elm.Dot().at((7, 4))
d += elm.Label().at((7.2, 4)).label('3.3V RAIL', fontsize=10, font='bold', halign='left')

# Ground connections
d += elm.Line().at((3, 3)).to((5, 3))
d += elm.Ground().at((3, 3))
d += elm.Label().at((4, 3.2)).label('GND', fontsize=8, halign='center')

# 5V Rail consumers (right side, upper section)
d += elm.Label().at((9, 6.5)).label('5V CONSUMERS:', fontsize=10, font='bold', halign='left')

# MCP4728 DAC
d += elm.Line().at((7, 5.5)).to((9, 5.5))
d += elm.Label().at((9.2, 5.5)).label('MCP4728 DAC (VDD)', fontsize=9, halign='left')
d += elm.Label().at((9.2, 5.2)).label('~1-5mA typical', fontsize=8, halign='left')

# Decoupling caps for 5V
d += elm.Line().at((9, 5.5)).down(0.3)
d += elm.Capacitor().down(0.5).label('C1\n47µF', fontsize=8, loc='right')
d += elm.Ground()
d += elm.Line().at((9.8, 5.2)).down(0.3)
d += elm.Capacitor().down(0.5).label('C2\n0.1µF', fontsize=8, loc='right')
d += elm.Ground()

# 3.3V Rail consumers (right side, lower section)
d += elm.Label().at((9, 3.5)).label('3.3V CONSUMERS:', fontsize=10, font='bold', halign='left')

# Consumer list
d += elm.Line().at((7, 4)).to((9, 4))
d += elm.Label().at((9.2, 4)).label('OLED FeatherWing (~20mA)', fontsize=8, halign='left')
d += elm.Label().at((9.2, 3.7)).label('MIDI FeatherWing (~15mA)', fontsize=8, halign='left')
d += elm.Label().at((9.2, 3.4)).label('4× White LEDs (~8mA)', fontsize=8, halign='left')
d += elm.Label().at((9.2, 3.1)).label('6× RGB channels (~20mA)', fontsize=8, halign='left')
d += elm.Label().at((9.2, 2.8)).label('BAT85 clamps (if used)', fontsize=8, halign='left')

# Decoupling caps for 3.3V
d += elm.Line().at((9, 2.5)).down(0.3)
d += elm.Capacitor().down(0.5).label('C9\n10µF', fontsize=8, loc='right')
d += elm.Ground()
d += elm.Line().at((9.8, 2.2)).down(0.3)
d += elm.Capacitor().down(0.5).label('C10\n0.1µF', fontsize=8, loc='right')
d += elm.Ground()

# Power budget summary (bottom)
d += elm.Label().at((0, 1.5)).label('POWER BUDGET:', fontsize=11, font='bold', halign='left')
d += elm.Label().at((0, 1.1)).label('USB Input: 5V @ 500mA min (USB 2.0), up to 3A (USB 3.0)', fontsize=9, halign='left')
d += elm.Label().at((0, 0.7)).label('5V Rail: ~5mA typical, ~50mA max', fontsize=9, halign='left')
d += elm.Label().at((0, 0.3)).label('3.3V Rail: ~65mA typical, ~100mA max', fontsize=9, halign='left')
d += elm.Label().at((0, -0.1)).label('Total Load: ~75mA typical, ~120mA max (4× margin)', fontsize=9, halign='left')

# Notes section (bottom right)
d += elm.Label().at((9, 1.5)).label('NOTES:', fontsize=10, font='bold', halign='left')
d += elm.Label().at((9, 1.1)).label('• NO battery or powerboost', fontsize=8, halign='left')
d += elm.Label().at((9, 0.8)).label('• USB-C power only', fontsize=8, halign='left')
d += elm.Label().at((9, 0.5)).label('• Simpler, cheaper, safer', fontsize=8, halign='left')
d += elm.Label().at((9, 0.2)).label('• 500mA USB 2.0 sufficient', fontsize=8, halign='left')
d += elm.Label().at((9, -0.1)).label('• Plenty of headroom', fontsize=8, halign='left')

# Save
d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/POWER_DISTRIBUTION.svg')
print("✅ Generated: POWER_DISTRIBUTION.svg (USB-only power system)")
