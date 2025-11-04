#!/usr/bin/env python3
"""
BOTTOM BOARD - DAC Outputs and S-TRIG Circuit
Clean, professional schematic using schemdraw best practices
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5)

    # ========== DAC OUTPUT CHANNEL 1 (VA) ==========
    d += elm.Dot().label('DAC VA', loc='left')
    d += elm.Resistor().right().label('R6 100ohm')
    d += elm.LED().right().label('LED1')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 1', loc='right')

    # Move down
    d.here = (0, d.here[1] - d.unit*1.5)

    # ========== DAC OUTPUT CHANNEL 2 (VB) ==========
    d += elm.Dot().label('DAC VB', loc='left')
    d += elm.Resistor().right().label('R7 100ohm')
    d += elm.LED().right().label('LED2')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 2', loc='right')

    # Move down
    d.here = (0, d.here[1] - d.unit*1.5)

    # ========== DAC OUTPUT CHANNEL 3 (VC) ==========
    d += elm.Dot().label('DAC VC', loc='left')
    d += elm.Resistor().right().label('R8 100ohm')
    d += elm.LED().right().label('LED3')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 3', loc='right')

    # Move down
    d.here = (0, d.here[1] - d.unit*1.5)

    # ========== DAC OUTPUT CHANNEL 4 (VD) ==========
    d += elm.Dot().label('DAC VD', loc='left')
    d += elm.Resistor().right().label('R9 100ohm')
    d += elm.LED().right().label('LED4')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 4', loc='right')

    # Move down
    d.here = (0, d.here[1] - d.unit*2)

    # ========== S-TRIG OUTPUT ==========
    d += elm.Dot().label('M4 D11', loc='left')
    d += elm.Resistor().right().label('R10 10kohm')
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1 2N3904')
    d.push()
    d += elm.Line().up(d.unit*0.5)
    d += elm.Vdd().label('5V')
    d.pop()
    d += elm.Line().down(d.unit*0.3)
    d += elm.Ground()
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    d += elm.Dot(open=True).label('S-TRIG OUT', loc='right')

d.save('BOTTOM_BOARD_SCHEMATIC_CLEAN.svg')
print("✓ Generated: BOTTOM_BOARD_SCHEMATIC_CLEAN.svg")
print("  - 4 DAC output channels (VA, VB, VC, VD)")
print("  - Each with LED indicator (R6-R9, LED1-LED4)")
print("  - S-Trig output with NPN transistor (Q1, R10)")
