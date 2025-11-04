#!/usr/bin/env python3
"""
PRISME COMPLETE SYSTEM - ACTUALLY PROPERLY CONNECTED
Every component has real wire connections, not floating boxes
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=10, unit=2.5, inches_per_unit=0.5)

    # ========== 5V POWER RAIL ==========
    d.here = (0, 12)
    d += elm.Line().right().length(d.unit*14)
    d.push()
    d += elm.Vdd().label('5V')
    d.pop()
    rail_5v = d.here[1]

    # ========== 3.3V POWER RAIL ==========
    d.here = (0, 10.5)
    d += elm.Line().right().length(d.unit*14)
    d.push()
    d += elm.Vdd().label('3.3V')
    d.pop()
    rail_3v3 = d.here[1]

    # ========== CV IN CIRCUIT ==========
    d.here = (0, 8)
    d += elm.Gap().label(['+', 'CV IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R1 10k')
    d += elm.Dot()
    cv_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R2 10k', loc='bot')
    cv_r2_bottom = d.here
    d.pop()
    # Wire from tap to M4
    d += elm.Line().right().length(d.unit*1.5)
    cv_to_m4 = d.here

    # ========== TRIG IN CIRCUIT ==========
    d.here = (0, 5)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R4 10k')
    d += elm.Dot()
    trig_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R5 10k', loc='bot')
    trig_r5_bottom = d.here
    d.pop()
    # Wire from tap to M4
    d += elm.Line().right().length(d.unit*1.5)
    trig_to_m4 = d.here

    # ========== FEATHER M4 ==========
    m4_x = d.unit*5
    m4_y = 6.5
    d.here = (m4_x, m4_y)
    d += elm.IcDIP(pins=8, size=(2, 3)).label('M4', fontsize=11)

    # Connect CV IN to M4 A3
    d += elm.Line().at(cv_to_m4).right().tox(m4_x - 0.5).label('A3', loc='top', fontsize=8)

    # Connect TRIG IN to M4 A4
    d += elm.Line().at(trig_to_m4).right().tox(m4_x - 0.5).label('A4', loc='top', fontsize=8)

    # M4 to 3.3V rail
    d += elm.Line().at((m4_x - 0.5, m4_y + 1)).up().toy(rail_3v3).label('3V3', loc='left', fontsize=8)

    # M4 to 5V rail
    d += elm.Line().at((m4_x + 0.5, m4_y + 1)).up().toy(rail_5v).label('USB', loc='right', fontsize=8)

    # ========== I2C BUS FROM M4 ==========
    i2c_x = m4_x + 2

    # SDA line
    d += elm.Line().at((m4_x + 1, m4_y + 0.3)).right().tox(i2c_x + 3)
    sda_y = d.here[1]
    d += elm.Dot().label('SDA', loc='top', fontsize=8)
    sda_end = d.here

    # SCL line
    d += elm.Line().at((m4_x + 1, m4_y - 0.3)).right().tox(i2c_x + 3)
    scl_y = d.here[1]
    d += elm.Dot().label('SCL', loc='bot', fontsize=8)
    scl_end = d.here

    # ========== MCP4728 DAC ==========
    dac_x = i2c_x + 1.5
    dac_y = m4_y
    d.here = (dac_x, dac_y)
    d += elm.IcDIP(pins=8, size=(1.5, 2.5)).label('MCP4728\nDAC', fontsize=9)

    # Connect DAC to I2C
    d += elm.Line().at((dac_x - 0.5, dac_y + 0.3)).left().tox(i2c_x + 3).dot()
    d += elm.Line().at((dac_x - 0.5, dac_y - 0.3)).left().tox(i2c_x + 3).dot()

    # DAC to 5V
    d += elm.Line().at((dac_x, dac_y + 1)).up().toy(rail_5v).label('VDD', loc='right', fontsize=8)

    # ========== DAC OUTPUTS ==========
    output_x = dac_x + 2

    # VA - CV OUT
    d += elm.Line().at((dac_x + 0.75, dac_y + 0.8)).right().length(d.unit*0.3).label('VA', loc='top', fontsize=8)
    d += elm.Resistor().right().label('100ohm', fontsize=8)
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CV OUT', loc='right')

    # VB - TRIG OUT
    d += elm.Line().at((dac_x + 0.75, dac_y + 0.3)).right().length(d.unit*0.3).label('VB', loc='top', fontsize=8)
    d += elm.Resistor().right().label('100ohm', fontsize=8)
    d += elm.Line().right()
    d += elm.Dot(open=True).label('TRIG OUT', loc='right')

    # VC - CC OUT
    d += elm.Line().at((dac_x + 0.75, dac_y - 0.3)).right().length(d.unit*0.3).label('VC', loc='bot', fontsize=8)
    d += elm.Resistor().right().label('100ohm', fontsize=8)
    d += elm.Line().right()
    d += elm.Dot(open=True).label('CC OUT', loc='right')

    # VD - Future
    d += elm.Line().at((dac_x + 0.75, dac_y - 0.8)).right().length(d.unit*0.3).label('VD', loc='bot', fontsize=8)
    d += elm.Line().right().length(d.unit*2)
    d += elm.Dot(open=True).label('Future', loc='right')

    # ========== S-TRIG OUTPUT ==========
    strig_y = 2
    d += elm.Line().at((m4_x + 0.5, m4_y - 1.5)).down().toy(strig_y).label('D10', loc='left', fontsize=8)
    d += elm.Resistor().right().label('1k', fontsize=8)
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1', fontsize=8)
    d.push()
    d += elm.Line().up().toy(rail_5v)
    d.pop()
    d.push()
    ground_y = 0
    d += elm.Line().down().toy(ground_y)
    d.pop()
    d += elm.Line().right().length(d.unit*1)
    d += elm.Dot(open=True).label('S-TRIG', loc='right')

    # ========== GROUND RAIL ==========
    d.here = (0, ground_y)
    d += elm.Line().right().length(d.unit*14)
    d += elm.Ground()

    # Connect input grounds
    d += elm.Line().at(cv_r2_bottom).down().toy(ground_y)
    d += elm.Line().at(trig_r5_bottom).down().toy(ground_y)

    # M4 ground
    d += elm.Line().at((m4_x, m4_y - 1.5)).down().toy(ground_y)

    # DAC ground
    d += elm.Line().at((dac_x, dac_y - 1.25)).down().toy(ground_y)

d.save('SYSTEM_ACTUALLY_CONNECTED.svg')
print("✓ Generated: SYSTEM_ACTUALLY_CONNECTED.svg")
print("  REAL connections:")
print("  - CV/TRIG inputs → voltage dividers → M4 pins A3/A4")
print("  - M4 SDA/SCL → I2C bus → DAC")
print("  - M4 power: USB(5V) and 3V3 rails")
print("  - DAC powered by 5V")
print("  - DAC outputs: VA/VB/VC/VD → resistors → jacks")
print("  - M4 D10 → S-TRIG transistor circuit")
print("  - All grounds connected to common rail")
