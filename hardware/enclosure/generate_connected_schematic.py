#!/usr/bin/env python3
"""
ACTUALLY CONNECTED SCHEMATIC
Shows the actual electrical connections, not just floating components
"""

import schemdraw
from schemdraw import elements as elm

d = schemdraw.Drawing()

# ============================================================================
# TOP BOARD - CV IN Protection Circuit
# ============================================================================

# CV IN - complete connected circuit
d += elm.Dot().at((0, 10)).label('CV IN', loc='left')
d += elm.Resistor().right().length(2).label('R1\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R2\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D1\nBAT85', loc='right', ofst=0.5)
d += elm.Line().down().length(1.5)  # Back to main line
d += elm.Dot().label('→ M4 A3', loc='right')

# ============================================================================
# TOP BOARD - TRIG IN Protection Circuit
# ============================================================================

# TRIG IN - complete connected circuit
d += elm.Dot().at((0, 6)).label('TRIG IN', loc='left')
d += elm.Resistor().right().length(2).label('R4\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R5\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D2\nBAT85', loc='right', ofst=0.5)
d += elm.Line().down().length(1.5)  # Back to main line
d += elm.Dot().label('→ M4 A4', loc='right')

# ============================================================================
# BOTTOM BOARD - DAC Output Channels
# ============================================================================

# Channel 1: VA → R6 → LED1 → CV OUT 1
d += elm.Dot().at((0, 2)).label('M4 D4 → DAC VA', loc='left')
d += elm.Resistor().right().length(2).label('R6\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED1', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 1', loc='right')

# Channel 2: VB → R7 → LED2 → CV OUT 2
d += elm.Dot().at((0, 0)).label('M4 D5 → DAC VB', loc='left')
d += elm.Resistor().right().length(2).label('R7\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED2', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 2', loc='right')

# Channel 3: VC → R8 → LED3 → CV OUT 3
d += elm.Dot().at((0, -2)).label('M4 D6 → DAC VC', loc='left')
d += elm.Resistor().right().length(2).label('R8\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED3', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 3', loc='right')

# Channel 4: VD → R9 → LED4 → CV OUT 4
d += elm.Dot().at((0, -4)).label('M4 D10 → DAC VD', loc='left')
d += elm.Resistor().right().length(2).label('R9\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED4', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 4', loc='right')

# Title
d += elm.Label().at((5, 12)).label('PRISME HARDWARE - COMPLETE CIRCUIT', fontsize=14, halign='center')
d += elm.Label().at((5, 11.2)).label('Signal Flow: LEFT → RIGHT', fontsize=10, halign='center')

d.save('CONNECTED_SCHEMATIC.svg')
print("✓ Generated: CONNECTED_SCHEMATIC.svg")
print("  Shows actual electrical connections")
print("  CV IN → Protection → M4 A3")
print("  TRIG IN → Protection → M4 A4")
print("  M4 D4/D5/D6/D10 → DAC → Resistors → LEDs → CV Outputs")
