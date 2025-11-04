#!/usr/bin/env python3
"""
BOTTOM BOARD - COMPLETE SCHEMATIC
Shows all 4 DAC outputs and S-TRIG circuit with shared power/ground rails
Using the clean approach that worked
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5)

    # 5V power rail at top
    d += elm.Line().right().length(d.unit*8)
    d.push()
    d += elm.Vdd().label('5V')
    d.pop()

    rail_top = d.here[1]

    # ========== DAC OUTPUT 1 (VA) ==========
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VA', loc='left')
    d += elm.Resistor().right().label('R6 100ohm')
    d += elm.LED().right().label('LED1')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 1', loc='right')

    # ========== DAC OUTPUT 2 (VB) ==========
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VB', loc='left')
    d += elm.Resistor().right().label('R7 100ohm')
    d += elm.LED().right().label('LED2')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 2', loc='right')

    # ========== DAC OUTPUT 3 (VC) ==========
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VC', loc='left')
    d += elm.Resistor().right().label('R8 100ohm')
    d += elm.LED().right().label('LED3')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 3', loc='right')

    # ========== DAC OUTPUT 4 (VD) ==========
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VD', loc='left')
    d += elm.Resistor().right().label('R9 100ohm')
    d += elm.LED().right().label('LED4')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 4', loc='right')

    # ========== S-TRIG OUTPUT ==========
    d.here = (0, d.here[1] - d.unit*2)
    d += elm.Dot().label('M4 D11', loc='left')
    d += elm.Resistor().right().label('R10 10kohm')
    d.push()
    q1_pos = d.here
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1 2N3904')
    d.push()
    d += elm.Line().up().toy(rail_top)
    d.pop()
    d.push()
    ground_pos = d.here[1] - d.unit*1.5
    d += elm.Line().down().toy(ground_pos)
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    d += elm.Dot(open=True).label('S-TRIG OUT', loc='right')

    # Common ground rail at bottom
    d.here = (0, ground_pos)
    d += elm.Line().right().length(d.unit*8)
    d += elm.Ground()

d.save('BOTTOM_BOARD_COMPLETE.svg')
print("✓ Generated: BOTTOM_BOARD_COMPLETE.svg")
print("  Complete bottom board with 4 DAC outputs + S-TRIG")
print("  Shared 5V power rail and ground rail")
