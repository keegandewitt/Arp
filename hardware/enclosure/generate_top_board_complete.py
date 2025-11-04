#!/usr/bin/env python3
"""
TOP BOARD - COMPLETE SCHEMATIC
Shows both CV IN and TRIG IN circuits on one schematic
Using the clean approach that worked
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5)

    # 3.3V power rail at top
    d += elm.Line().right().length(d.unit*6)
    d.push()
    d += elm.Vdd().label('3.3V')
    d.pop()

    # ========== CV IN CIRCUIT ==========
    # Input jack
    cv_start = d.here
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Gap().label(['+', 'CV IN', '−'])

    # Voltage divider
    d.push()
    d += elm.Resistor().right().label('R1\n10kΩ')
    d += elm.Dot()
    tap1 = d.here
    d.push()
    d += elm.Resistor().down().label('R2\n10kΩ', loc='bot')
    r2_bottom = d.here
    d.pop()

    # BAT85 clamp to 3.3V rail
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D1\nBAT85')
    d += elm.Line().toy(cv_start[1])
    d.pop()

    # To M4 ADC
    d += elm.Line().right()
    d += elm.Dot(open=True).label('M4 A3', loc='right')

    # ========== TRIG IN CIRCUIT ==========
    # Position TRIG IN to the left, below CV IN
    d.here = (0, r2_bottom[1] - d.unit*1.5)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])

    # Voltage divider
    d.push()
    d += elm.Resistor().right().label('R4\n10kΩ')
    d += elm.Dot()
    tap2 = d.here
    d.push()
    d += elm.Resistor().down().label('R5\n10kΩ', loc='bot')
    r5_bottom = d.here
    d.pop()

    # BAT85 clamp to 3.3V rail
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D2\nBAT85')
    d += elm.Line().toy(cv_start[1])
    d.pop()

    # To M4 ADC
    d += elm.Line().right().tox(tap1[0] + d.unit*2)
    d += elm.Dot(open=True).label('M4 A4', loc='right')

    # Common ground rail at bottom
    d.here = (0, r5_bottom[1] - d.unit*0.5)
    d += elm.Line().right().length(d.unit*6)
    d += elm.Ground()

    # Connect R2 and R5 to ground rail
    d += elm.Line().at(r2_bottom).down().toy(r5_bottom[1] - d.unit*0.5)
    d += elm.Line().at(r5_bottom).down().toy(r5_bottom[1] - d.unit*0.5)

d.save('TOP_BOARD_COMPLETE.svg')
print("✓ Generated: TOP_BOARD_COMPLETE.svg")
print("  Complete top board with both CV IN and TRIG IN circuits")
