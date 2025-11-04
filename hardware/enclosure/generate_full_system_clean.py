#!/usr/bin/env python3
"""
FULL SYSTEM SCHEMATIC - CLEAN AND SPACED
Uses the SIMPLE approach that actually works: .length() for spacing, ofst for labels
"""

import schemdraw
from schemdraw import elements as elm

d = schemdraw.Drawing()

# ============================================================================
# TOP BOARD - CV IN and TRIG IN (with protection)
# ============================================================================

# CV IN circuit (Row 1)
d += elm.Dot().at((0, 14)).label('CV IN', loc='left')
d += elm.Resistor().right().length(2).label('R1\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R2\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D1\nBAT85', loc='right', ofst=0.5)
d += elm.Line().at((8, 14)).right().length(2)
d += elm.Dot().label('M4 A3', loc='right', ofst=0.3)

# TRIG IN circuit (Row 2)
d += elm.Dot().at((0, 11)).label('TRIG IN', loc='left')
d += elm.Resistor().right().length(2).label('R4\n10kΩ', loc='top', ofst=0.5)
d += elm.Resistor().right().length(2).label('R5\n10kΩ', loc='top', ofst=0.5)
d += elm.Diode().up().length(1.5).label('D2\nBAT85', loc='right', ofst=0.5)
d += elm.Line().at((8, 11)).right().length(2)
d += elm.Dot().label('M4 A4', loc='right', ofst=0.3)

# Top board label
d += elm.Label().at((5, 16)).label('TOP BOARD: INPUT PROTECTION', fontsize=12, halign='center')

# ============================================================================
# CENTER - M4 MICROCONTROLLER
# ============================================================================

# Simple box representing M4
d += elm.IcDIP(pins=8).at((13, 12.5)).label('Feather M4 CAN', fontsize=11)

# (Section separation provided by vertical spacing)

# ============================================================================
# BOTTOM BOARD - DAC OUTPUTS
# ============================================================================

# DAC representation
d += elm.IcDIP(pins=8).at((13, 6)).label('MCP4728 DAC', fontsize=11)

# Output Row 1: VA (CV OUT 1)
d += elm.Dot().at((18, 7.5)).label('VA', loc='left', ofst=0.3)
d += elm.Resistor().right().length(2).label('R6\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED1', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 1', loc='right')

# Output Row 2: VB (CV OUT 2)
d += elm.Dot().at((18, 6.5)).label('VB', loc='left', ofst=0.3)
d += elm.Resistor().right().length(2).label('R7\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED2', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 2', loc='right')

# Output Row 3: VC (CV OUT 3)
d += elm.Dot().at((18, 5.5)).label('VC', loc='left', ofst=0.3)
d += elm.Resistor().right().length(2).label('R8\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED3', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 3', loc='right')

# Output Row 4: VD (CV OUT 4)
d += elm.Dot().at((18, 4.5)).label('VD', loc='left', ofst=0.3)
d += elm.Resistor().right().length(2).label('R9\n100Ω', loc='top', ofst=0.5)
d += elm.LED().right().label('LED4', loc='top', ofst=0.5)
d += elm.Line().right().length(1)
d += elm.Dot().label('CV OUT 4', loc='right')

# Bottom board label
d += elm.Label().at((21, 3)).label('BOTTOM BOARD: DAC + LED INDICATORS', fontsize=12, halign='center')

# ============================================================================
# CONNECTIONS - Show signal flow
# ============================================================================

# M4 to DAC control (I2C)
d += elm.Line().at((13, 8.5)).down().length(1.5).label('I2C', loc='right', ofst=0.3, fontsize=9)

# Title
d += elm.Label().at((13, 18)).label('PRISME HARDWARE SYSTEM', fontsize=14, halign='center')

d.save('FULL_SYSTEM_CLEAN.svg')
print("✓ Generated: FULL_SYSTEM_CLEAN.svg")
print("  - TOP BOARD: CV/TRIG inputs with protection")
print("  - M4: Feather M4 CAN microcontroller")
print("  - BOTTOM BOARD: MCP4728 DAC with 4 output channels")
print("  - Clean spacing with .length(2) and ofst=0.5")
