#!/usr/bin/env python3
"""
CLEAN CV IN PROTECTION CIRCUIT
Based on actual schemdraw gallery examples
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5)

    # Input jack
    d += elm.Gap().label(['+', 'CV IN', '−'])

    # Voltage divider
    d.push()
    d += elm.Resistor().right().label('R1\n10kΩ')
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R2\n10kΩ', loc='bot')
    d += elm.Ground()
    d.pop()

    # BAT85 clamp to 3.3V rail
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D1\nBAT85')
    d += elm.Line().up(d.unit*0.3)
    d += elm.Vdd().label('3.3V')
    d.pop()

    # To M4 ADC
    d += elm.Line().right()
    d += elm.Dot(open=True).label('M4 A3', loc='right')

    d.pop()
    d += elm.Line().down()
    d += elm.Ground()

d.save('CV_IN_CLEAN.svg')
print("✓ Generated: CV_IN_CLEAN.svg")
