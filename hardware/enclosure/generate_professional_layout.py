#!/usr/bin/env python3
"""
PROFESSIONAL LAYOUT - Copy the buzzer schematic structure EXACTLY
- Horizontal power rail at top
- Horizontal ground rail at bottom
- Components flow left to right between the rails
- Everything actually connected
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=10, unit=2)

    # ========== POWER RAILS ==========
    # 5V rail across entire top
    d.here = (0, 10)
    d += elm.Line().right().length(20)
    d.push()
    d += elm.Vdd().label('5V')
    d.pop()

    # 3.3V rail below it
    d.here = (0, 9)
    d += elm.Line().right().length(20)
    d.push()
    d += elm.Vdd().label('3.3V')
    d.pop()

    # ========== CV IN - Left side ==========
    d.here = (0, 7)
    d += elm.Gap().label(['+', 'CV IN', '−'])
    d.push()
    # Voltage divider
    d += elm.Resistor().right().label('10k')
    d += elm.Dot()
    tap1 = d.here
    d.push()
    d += elm.Resistor().down().label('10k', loc='bot')
    gnd1 = d.here
    d.pop()
    # Continue to M4
    d += elm.Line().right().length(1)
    to_m4_a3 = d.here

    # ========== TRIG IN - Left side below CV IN ==========
    d.here = (0, 4)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])
    d.push()
    # Voltage divider
    d += elm.Resistor().right().label('10k')
    d += elm.Dot()
    tap2 = d.here
    d.push()
    d += elm.Resistor().down().label('10k', loc='bot')
    gnd2 = d.here
    d.pop()
    # Continue to M4
    d += elm.Line().right().length(1)
    to_m4_a4 = d.here

    # ========== DAC OUTPUTS - Right side ==========
    # CV OUT
    d.here = (14, 7.5)
    d += elm.Resistor().right().label('100ohm')
    d += elm.LED().right()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT', loc='right')

    # TRIG OUT
    d.here = (14, 6)
    d += elm.Resistor().right().label('100ohm')
    d += elm.LED().right()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('TRIG OUT', loc='right')

    # CC OUT
    d.here = (14, 4.5)
    d += elm.Resistor().right().label('100ohm')
    d += elm.LED().right()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CC OUT', loc='right')

    # ========== S-TRIG ==========
    d.here = (14, 2)
    d += elm.Resistor().right().label('1k')
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base')
    d.push()
    d += elm.Line().up().toy(10)
    d.pop()
    q_gnd = d.here
    d += elm.Line().down().length(2)
    d.pop()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('S-TRIG', loc='right')

    # ========== GROUND RAIL ==========
    d.here = (0, 0)
    d += elm.Line().right().length(20)
    d += elm.Ground()

    # Connect grounds
    d += elm.Line().at(gnd1).down().toy(0)
    d += elm.Line().at(gnd2).down().toy(0)

d.save('PROFESSIONAL_LAYOUT.svg')
print("✓ Generated: PROFESSIONAL_LAYOUT.svg")
