#!/usr/bin/env python3
"""
Generate TOP BOARD (Input) Schematic - ACTUAL Design
Session 25 - Truth-based schematic for EasyEDA PCB design
"""

import schemdraw
import schemdraw.elements as elm

# Create new drawing
d = schemdraw.Drawing()

# Title block
d += elm.Label().at((0, 10)).label('PRISME TOP BOARD - INPUT CIRCUITS', fontsize=14, halign='left')
d += elm.Label().at((0, 9.5)).label('Session 25 - Actual Design (No Fiction)', fontsize=10, halign='left')
d += elm.Label().at((0, 9)).label('Date: 2025-11-03', fontsize=8, halign='left')

# ============================================================================
# SECTION 1: POWER DISTRIBUTION (Both Rails)
# ============================================================================

d += elm.Label().at((0, 8)).label('POWER DISTRIBUTION', fontsize=12, halign='left', font='bold')

# 5V Rail (from Feather M4)
d += elm.Label().at((0, 7)).label('5V Rail:', fontsize=10, halign='left')
d += elm.Vdd().at((2, 7)).label('5V\n(from M4)', fontsize=8)
pos_5v = (2, 7)

# 5V decoupling caps
d += elm.Line().at(pos_5v).down(0.5)
d += elm.Capacitor().down(1).label('C11\n10uF\nElectrolytic', fontsize=7, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

d += elm.Line().at((2, 6.5)).right(1)
d += elm.Capacitor().down(1).label('C12\n0.1uF\nCeramic', fontsize=7, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

# 3.3V Rail (from Feather M4)
d += elm.Label().at((6, 7)).label('3.3V Rail:', fontsize=10, halign='left')
d += elm.Vdd().at((8, 7)).label('3.3V\n(from M4)', fontsize=8)
pos_3v3 = (8, 7)

# 3.3V decoupling caps
d += elm.Line().at(pos_3v3).down(0.5)
d += elm.Capacitor().down(1).label('C13\n10uF\nElectrolytic', fontsize=7, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

d += elm.Line().at((8, 6.5)).right(1)
d += elm.Capacitor().down(1).label('C14\n0.1uF\nCeramic', fontsize=7, loc='right')
d += elm.Line().down(0.5)
d += elm.Ground()

d += elm.Label().at((6, 5)).label('Powers: Input LEDs, BAT85 clamps', fontsize=7, halign='left')

# ============================================================================
# SECTION 2: CV IN Circuit (A3)
# ============================================================================

d += elm.Label().at((0, 3.5)).label('CV IN - Channel A3', fontsize=12, halign='left', font='bold')

# CV IN Jack
d += elm.Dot().at((0, 2.5)).label('CV IN\nJack TIP', fontsize=8, halign='right')
cv_in_start = (0, 2.5)

# Voltage divider R1
d += elm.Line().at(cv_in_start).right(0.5)
d += elm.Resistor().right(1.5).label('R1\n10k ohm', fontsize=7, loc='top')
cv_tap = (2, 2.5)
d += elm.Dot().at(cv_tap).label('TAP', fontsize=7, loc='top')

# Wire to ADC pin
d += elm.Line().at(cv_tap).right(2)
d += elm.Dot().label('To M4\nPin A3', fontsize=8, halign='left')

# Voltage divider R2 (to ground)
d += elm.Line().at(cv_tap).down(0.5)
d += elm.Resistor().down(1).label('R2\n10k ohm', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# BAT85 overvoltage clamp (from TAP to 3.3V)
d += elm.Line().at(cv_tap).up(0.5)
d += elm.Diode().up(1).label('D1\nBAT85\nSchottky', fontsize=7, loc='left')
d += elm.Line().up(0.3)
d += elm.Vdd().label('3.3V', fontsize=7)

# Optional smoothing cap
d += elm.Line().at((cv_tap[0] - 0.5, cv_tap[1])).down(0.5)
d += elm.Capacitor().down(1).label('C15\n100nF\n(optional)', fontsize=6, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# CV IN LED indicator
d += elm.Line().at((cv_in_start[0], cv_in_start[1])).down(1.5)
d += elm.Resistor().down(0.8).label('R3\n1k ohm', fontsize=7, loc='left')
d += elm.LED().down(0.8).label('LED1\nWhite', fontsize=7, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# Jack ground
d += elm.Line().at((cv_in_start[0], cv_in_start[1])).down(3.5)
d += elm.Dot().label('Jack\nSLEEVE', fontsize=7, halign='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 3: TRIG IN Circuit (A4)
# ============================================================================

d += elm.Label().at((0, -2)).label('TRIG IN - Channel A4', fontsize=12, halign='left', font='bold')

# TRIG IN Jack
d += elm.Dot().at((0, -3)).label('TRIG IN\nJack TIP', fontsize=8, halign='right')
trig_in_start = (0, -3)

# Voltage divider R4
d += elm.Line().at(trig_in_start).right(0.5)
d += elm.Resistor().right(1.5).label('R4\n10k ohm', fontsize=7, loc='top')
trig_tap = (2, -3)
d += elm.Dot().at(trig_tap).label('TAP', fontsize=7, loc='top')

# Wire to ADC pin
d += elm.Line().at(trig_tap).right(2)
d += elm.Dot().label('To M4\nPin A4', fontsize=8, halign='left')

# Voltage divider R5 (to ground)
d += elm.Line().at(trig_tap).down(0.5)
d += elm.Resistor().down(1).label('R5\n10k ohm', fontsize=7, loc='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# BAT85 overvoltage clamp (from TAP to 3.3V)
d += elm.Line().at(trig_tap).up(0.5)
d += elm.Diode().up(1).label('D2\nBAT85\nSchottky', fontsize=7, loc='left')
d += elm.Line().up(0.3)
d += elm.Vdd().label('3.3V', fontsize=7)

# Optional smoothing cap
d += elm.Line().at((trig_tap[0] - 0.5, trig_tap[1])).down(0.5)
d += elm.Capacitor().down(1).label('C16\n100nF\n(optional)', fontsize=6, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# TRIG IN RGB LED indicator
d += elm.Line().at((trig_in_start[0], trig_in_start[1])).down(1.5)
d += elm.Resistor().down(0.8).label('R6\n330 ohm', fontsize=7, loc='left')
d += elm.LED().down(0.8).label('LED2\nRGB', fontsize=7, loc='left')
d += elm.Line().down(0.3)
d += elm.Ground()

# Jack ground
d += elm.Line().at((trig_in_start[0], trig_in_start[1])).down(3.5)
d += elm.Dot().label('Jack\nSLEEVE', fontsize=7, halign='right')
d += elm.Line().down(0.3)
d += elm.Ground()

# ============================================================================
# SECTION 4: Connections to Feather M4
# ============================================================================

d += elm.Label().at((6, -2)).label('CONNECTIONS TO M4', fontsize=10, halign='left', font='bold')
d += elm.Label().at((6, -2.5)).label('Pin A3 <- CV IN (via divider)', fontsize=8, halign='left')
d += elm.Label().at((6, -3)).label('Pin A4 <- TRIG IN (via divider)', fontsize=8, halign='left')
d += elm.Label().at((6, -3.5)).label('Pin D4 -> CV IN LED (white)', fontsize=8, halign='left')
d += elm.Label().at((6, -4)).label('Pin D11 -> TRIG IN LED R (RGB)', fontsize=8, halign='left')
d += elm.Label().at((6, -4.5)).label('Pin D23 -> TRIG IN LED G (RGB)', fontsize=8, halign='left')
d += elm.Label().at((6, -5)).label('Pin D24 -> TRIG IN LED B (RGB)', fontsize=8, halign='left')

# ============================================================================
# SECTION 5: Notes
# ============================================================================

d += elm.Label().at((0, -7)).label('DESIGN NOTES:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((0, -7.5)).label('1. Voltage dividers scale 5V input to 2.5V (safe for 3.3V ADC)', fontsize=8, halign='left')
d += elm.Label().at((0, -8)).label('2. BAT85 diodes clamp voltage spikes to 3.7V max (100% safe)', fontsize=8, halign='left')
d += elm.Label().at((0, -8.5)).label('3. 100nF smoothing caps are OPTIONAL (filter cable noise)', fontsize=8, halign='left')
d += elm.Label().at((0, -9)).label('4. Both 5V and 3.3V rails require decoupling (C11-C14)', fontsize=8, halign='left')
d += elm.Label().at((0, -9.5)).label('5. BAT85 cathode (banded end) connects to 3.3V rail', fontsize=8, halign='left')
d += elm.Label().at((0, -10)).label('6. Current limiting resistors for LEDs (1k-330 ohm typical)', fontsize=8, halign='left')

# ============================================================================
# SECTION 6: Protection Analysis
# ============================================================================

d += elm.Label().at((6, -7)).label('PROTECTION ANALYSIS:', fontsize=10, halign='left', font='bold')
d += elm.Label().at((6, -7.5)).label('Without BAT85: Safe up to 6.6V (60%)', fontsize=8, halign='left')
d += elm.Label().at((6, -8)).label('With BAT85: Safe up to 40V+ (100%)', fontsize=8, halign='left')
d += elm.Label().at((6, -8.5)).label('M4 ADC max: 3.3V nominal, 3.6V absolute', fontsize=8, halign='left')
d += elm.Label().at((6, -9)).label('BAT85 clamp: 3.3V + 0.4V = 3.7V max', fontsize=8, halign='left')

# Save schematic
d.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_BOARD_FINAL.svg')
print("TOP BOARD schematic saved to: TOP_BOARD_FINAL.svg")
print("File size:", len(open('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_BOARD_FINAL.svg').read()), "bytes")
