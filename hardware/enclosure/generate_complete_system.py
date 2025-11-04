#!/usr/bin/env python3
"""
COMPLETE SYSTEM SCHEMATIC
Shows entire PRISME hardware: inputs, M4, DAC, outputs
Using the clean approach that worked for individual boards
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=2.5, inches_per_unit=0.5)

    # ========== POWER RAILS ==========
    # 5V rail at very top
    d += elm.Line().right().length(d.unit*12)
    d.push()
    d += elm.Vdd().label('5V')
    d.pop()
    rail_5v = d.here[1]

    # 3.3V rail below 5V
    d.here = (0, d.here[1] - d.unit*0.8)
    d += elm.Line().right().length(d.unit*12)
    d.push()
    d += elm.Vdd().label('3.3V')
    d.pop()
    rail_3v3 = d.here[1]

    # ========== CV IN CIRCUIT ==========
    d.here = (0, d.here[1] - d.unit*1.5)
    d += elm.Gap().label(['+', 'CV IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R1\n10kΩ')
    d += elm.Dot()
    cv_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R2\n10kΩ', loc='bot')
    cv_r2_bottom = d.here
    d.pop()
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D1\nBAT85')
    d += elm.Line().toy(rail_3v3)
    d.pop()
    d += elm.Line().right()
    d += elm.Dot(open=True).label('M4 A3', loc='right')

    # ========== TRIG IN CIRCUIT ==========
    d.here = (0, cv_r2_bottom[1] - d.unit*1.5)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R4\n10kΩ')
    d += elm.Dot()
    trig_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R5\n10kΩ', loc='bot')
    trig_r5_bottom = d.here
    d.pop()
    d += elm.Line().right()
    d.push()
    d += elm.Diode().up().label('D2\nBAT85')
    d += elm.Line().toy(rail_3v3)
    d.pop()
    d += elm.Line().right().tox(cv_tap[0] + d.unit*2)
    d += elm.Dot(open=True).label('M4 A4', loc='right')

    # ========== POWERBOOST (LEFT SIDE) ==========
    pb_x = d.unit*1
    pb_y = rail_5v - d.unit*2
    d.here = (pb_x, pb_y)
    d += elm.IcDIP(pins=4).label('PowerBoost\n5V', fontsize=10)

    # ========== M4 MICROCONTROLLER (CENTER) ==========
    m4_x = d.unit*5
    m4_y = (cv_tap[1] + trig_r5_bottom[1]) / 2
    d.here = (m4_x, m4_y)
    d += elm.IcDIP(pins=8).label('Feather M4', fontsize=10)

    # ========== DAC (CENTER-RIGHT) ==========
    dac_x = m4_x + d.unit*2.5
    dac_y = m4_y
    d.here = (dac_x, dac_y)
    d += elm.IcDIP(pins=8).label('MCP4728\nDAC', fontsize=10)

    # ========== DAC OUTPUTS ==========
    # Position DAC outputs on right side
    output_x = dac_x + d.unit*2.5

    # DAC VA
    d.here = (output_x, m4_y + d.unit*1.5)
    d += elm.Dot().label('VA', loc='left')
    d += elm.Resistor().right().label('R6\n100ohm')
    d += elm.LED().right().label('LED1')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 1', loc='right')

    # DAC VB
    d.here = (output_x, m4_y + d.unit*0.5)
    d += elm.Dot().label('VB', loc='left')
    d += elm.Resistor().right().label('R7\n100ohm')
    d += elm.LED().right().label('LED2')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 2', loc='right')

    # DAC VC
    d.here = (output_x, m4_y - d.unit*0.5)
    d += elm.Dot().label('VC', loc='left')
    d += elm.Resistor().right().label('R8\n100ohm')
    d += elm.LED().right().label('LED3')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 3', loc='right')

    # DAC VD
    d.here = (output_x, m4_y - d.unit*1.5)
    d += elm.Dot().label('VD', loc='left')
    d += elm.Resistor().right().label('R9\n100ohm')
    d += elm.LED().right().label('LED4')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT 4', loc='right')

    # ========== S-TRIG OUTPUT ==========
    d.here = (output_x, m4_y - d.unit*3)
    d += elm.Dot().label('D11', loc='left')
    d += elm.Resistor().right().label('R10\n10kohm')
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1 2N3904')
    d.push()
    d += elm.Line().up().toy(rail_5v)
    d.pop()
    d.push()
    ground_level = trig_r5_bottom[1] - d.unit*2
    d += elm.Line().down().toy(ground_level)
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    d += elm.Dot(open=True).label('S-TRIG OUT', loc='right')

    # ========== GROUND RAIL AT BOTTOM ==========
    d.here = (0, ground_level)
    d += elm.Line().right().length(d.unit*12)
    d += elm.Ground()

    # Connect input ground points to ground rail
    d += elm.Line().at(cv_r2_bottom).down().toy(ground_level)
    d += elm.Line().at(trig_r5_bottom).down().toy(ground_level)

d.save('COMPLETE_SYSTEM_SCHEMATIC.svg')
print("✓ Generated: COMPLETE_SYSTEM_SCHEMATIC.svg")
print("  Complete system: CV IN, TRIG IN, M4, DAC outputs, S-TRIG")
print("  Shared power rails (5V, 3.3V) and ground")
