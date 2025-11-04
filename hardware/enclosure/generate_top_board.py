#!/usr/bin/env python3
"""
TOP BOARD - CV IN and TRIG IN Protection Circuits
Clean, professional schematic using schemdraw best practices
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5)

    # ========== CV IN CIRCUIT ==========
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

    # Move down for next circuit
    d.here = (0, d.here[1] - d.unit*3)

    # ========== TRIG IN CIRCUIT ==========
    # Input jack
    d += elm.Gap().label(['+', 'TRIG IN', '−'])

    # Voltage divider
    d.push()
    d += elm.Resistor().right().label('R4\n10kΩ')
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R5\n10kΩ', loc='bot')
    d += elm.Ground()
    d.pop()

    # BAT85 clamp to 3.3V rail
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D2\nBAT85')
    d += elm.Line().up(d.unit*0.3)
    d += elm.Vdd().label('3.3V')
    d.pop()

    # To M4 ADC
    d += elm.Line().right()
    d += elm.Dot(open=True).label('M4 A4', loc='right')

    d.pop()
    d += elm.Line().down()
    d += elm.Ground()

d.save('TOP_BOARD_SCHEMATIC_CLEAN.svg')
print("✓ Generated: TOP_BOARD_SCHEMATIC_CLEAN.svg")
print("  - CV IN protection circuit (R1, R2, D1)")
print("  - TRIG IN protection circuit (R4, R5, D2)")
print("  - Both with BAT85 clamps to 3.3V rail")
