#!/usr/bin/env python3
"""
SIMPLE SCHEMATIC WITH ACTUAL SPACING
Just make things NOT overlap. That's it.
"""

import schemdraw
from schemdraw import elements as elm

d = schemdraw.Drawing()

# ROW 1: CV IN (with actual space between components)
d += elm.Dot().at((0, 10)).label('CV IN', loc='left')
d += elm.Resistor().right().length(2).label('R1\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R2\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D1\nBAT85', loc='right', ofst=0.5)
d += elm.Line().at((8, 10)).right().length(2)
d += elm.Dot().label('To M4 A3', loc='right')

# ROW 2: TRIG IN (with actual space between components)
d += elm.Dot().at((0, 6)).label('TRIG IN', loc='left')
d += elm.Resistor().right().length(2).label('R4\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R5\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D2\nBAT85', loc='right', ofst=0.5)
d += elm.Line().at((8, 6)).right().length(2)
d += elm.Dot().label('To M4 A4', loc='right')

# ROW 3: M4 (simple box)
d += elm.IcDIP(pins=4).at((12, 8)).label('M4', fontsize=14)

# ROW 4: Outputs (with actual space)
d += elm.Resistor().at((18, 10)).right().length(2).label('R6\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED', loc='top', ofst=0.5)
d += elm.Dot().label('CV OUT', loc='right')

d += elm.Resistor().at((18, 6)).right().length(2).label('R7\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED', loc='top', ofst=0.5)
d += elm.Dot().label('TRIG OUT', loc='right')

d.save('SIMPLE_SPACED.svg')
print("Done: SIMPLE_SPACED.svg")
