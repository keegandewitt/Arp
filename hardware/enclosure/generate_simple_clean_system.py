#!/usr/bin/env python3
"""
SIMPLE CLEAN SYSTEM - Build from what WORKS
Starting with CV_IN pattern and adding components methodically
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=10, unit=2.5, inches_per_unit=0.5)

    # Start simple - just the two input circuits stacked
    # Use the EXACT pattern that worked for CV_IN_CLEAN

    # CV IN circuit
    d += elm.Gap().label(['+', 'CV IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R1 10k')
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R2 10k', loc='bot')
    d += elm.Ground()
    d.pop()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('→ M4 A3', loc='right')
    d.pop()
    d += elm.Line().down()
    d += elm.Ground()

    # TRIG IN circuit - positioned below
    d.here = (0, d.here[1] - d.unit*3)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R4 10k')
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R5 10k', loc='bot')
    d += elm.Ground()
    d.pop()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('→ M4 A4', loc='right')
    d.pop()
    d += elm.Line().down()
    d += elm.Ground()

    # DAC output circuits - positioned below
    d.here = (0, d.here[1] - d.unit*4)

    # VA output
    d += elm.Dot().label('DAC VA', loc='left')
    d += elm.Resistor().right().label('R6 100ohm')
    d += elm.LED().right().label('LED1')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT', loc='right')

    # VB output
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VB', loc='left')
    d += elm.Resistor().right().label('R7 100ohm')
    d += elm.LED().right().label('LED2')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('TRIG OUT', loc='right')

    # VC output
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Dot().label('DAC VC', loc='left')
    d += elm.Resistor().right().label('R8 100ohm')
    d += elm.LED().right().label('LED3')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CC OUT', loc='right')

    # S-TRIG circuit
    d.here = (0, d.here[1] - d.unit*2)
    d += elm.Dot().label('M4 D10', loc='left')
    d += elm.Resistor().right().label('R10 1k')
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1')
    d.push()
    d += elm.Line().up(d.unit*0.5)
    d += elm.Vdd().label('5V')
    d.pop()
    d += elm.Line().down(d.unit*0.5)
    d += elm.Ground()
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    d += elm.Dot(open=True).label('S-TRIG OUT', loc='right')

d.save('SIMPLE_CLEAN_SYSTEM.svg')
print("✓ Generated: SIMPLE_CLEAN_SYSTEM.svg")
print("  Using the proven clean pattern from CV_IN_CLEAN")
print("  All circuits properly spaced vertically")
print("  No IC boxes to cause overlap")
