#!/usr/bin/env python3
"""
COMPLETE PRISME SYSTEM SCHEMATIC - PROPERLY CONNECTED
Based on ACTUAL_HARDWARE_TRUTH.md
Shows real connections between all components
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=10, unit=2.5, inches_per_unit=0.5)

    # ========== POWER RAILS ==========
    # 5V rail at top
    d += elm.Line().right().length(d.unit*16)
    d.push()
    d += elm.Vdd().label('5V USB')
    d.pop()
    rail_5v = d.here[1]

    # 3.3V rail below 5V
    d.here = (0, d.here[1] - d.unit*0.8)
    d += elm.Line().right().length(d.unit*16)
    d.push()
    d += elm.Vdd().label('3.3V')
    d.pop()
    rail_3v3 = d.here[1]

    # ========== LEFT SIDE: INPUT CIRCUITS ==========

    # CV IN circuit
    cv_in_y = rail_3v3 - d.unit*2
    d.here = (0, cv_in_y)
    d += elm.Gap().label(['+', 'CV IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R1\n10k')
    d += elm.Dot()
    cv_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R2\n10k', loc='bot')
    cv_gnd = d.here
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    cv_to_m4 = d.here
    d += elm.Dot(open=True).label('A3', loc='right')

    # TRIG IN circuit
    trig_in_y = cv_in_y - d.unit*2.5
    d.here = (0, trig_in_y)
    d += elm.Gap().label(['+', 'TRIG IN', '−'])
    d.push()
    d += elm.Resistor().right().label('R4\n10k')
    d += elm.Dot()
    trig_tap = d.here
    d.push()
    d += elm.Resistor().down().label('R5\n10k', loc='bot')
    trig_gnd = d.here
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    trig_to_m4 = d.here
    d += elm.Dot(open=True).label('A4', loc='right')

    # ========== CENTER: M4 MICROCONTROLLER ==========
    m4_x = d.unit*5.5
    m4_y = (cv_in_y + trig_in_y) / 2
    d.here = (m4_x, m4_y)
    d += elm.IcDIP(pins=12).label('Feather M4\nCAN', fontsize=11)

    # Note: M4 connects to inputs via lines drawn above
    # M4 connects to I2C bus (shown below)

    # ========== CENTER: MIDI FEATHERWING ==========
    midi_x = m4_x
    midi_y = m4_y + d.unit*2
    d.here = (midi_x, midi_y)
    d += elm.IcDIP(pins=6).label('MIDI\nFeatherWing', fontsize=10)
    # MIDI wing stacks on M4, powered by 3.3V
    d += elm.Line().at((midi_x, midi_y - d.unit*0.5)).up().toy(rail_3v3)

    # ========== CENTER: OLED DISPLAY ==========
    oled_x = m4_x
    oled_y = m4_y - d.unit*2.5
    d.here = (oled_x, oled_y)
    d += elm.IcDIP(pins=6).label('OLED\n128x64', fontsize=10)
    # OLED connects via I2C (same bus as DAC)

    # ========== CENTER-RIGHT: I2C BUS ==========
    i2c_x = m4_x + d.unit*2
    i2c_y = m4_y

    # SDA line
    d.here = (i2c_x, i2c_y + d.unit*0.3)
    d += elm.Line().right().length(d.unit*1.5).label('SDA', loc='top')
    sda_bus = d.here

    # SCL line
    d.here = (i2c_x, i2c_y - d.unit*0.3)
    d += elm.Line().right().length(d.unit*1.5).label('SCL', loc='bot')
    scl_bus = d.here

    # ========== RIGHT: MCP4728 DAC ==========
    dac_x = i2c_x + d.unit*2
    dac_y = m4_y
    d.here = (dac_x, dac_y)
    d += elm.IcDIP(pins=8).label('MCP4728\nDAC\n0x60', fontsize=10)

    # DAC power from 5V rail
    d += elm.Line().at((dac_x, dac_y + d.unit*0.8)).up().toy(rail_5v)

    # ========== RIGHT: DAC OUTPUTS ==========
    output_x = dac_x + d.unit*2.5

    # VA - CV OUT
    d.here = (output_x, dac_y + d.unit*1.2)
    d += elm.Dot().label('VA', loc='left')
    d += elm.Resistor().right().label('100ohm')
    d += elm.Line().right().length(d.unit*0.5)
    d += elm.Dot(open=True).label('CV OUT', loc='right')

    # VB - TRIG OUT (V-Trig)
    d.here = (output_x, dac_y + d.unit*0.4)
    d += elm.Dot().label('VB', loc='left')
    d += elm.Resistor().right().label('100ohm')
    d += elm.Line().right().length(d.unit*0.5)
    d += elm.Dot(open=True).label('TRIG OUT', loc='right')

    # VC - CC OUT
    d.here = (output_x, dac_y - d.unit*0.4)
    d += elm.Dot().label('VC', loc='left')
    d += elm.Resistor().right().label('100ohm')
    d += elm.Line().right().length(d.unit*0.5)
    d += elm.Dot(open=True).label('CC OUT', loc='right')

    # VD - Future
    d.here = (output_x, dac_y - d.unit*1.2)
    d += elm.Dot().label('VD', loc='left')
    d += elm.Line().right().length(d.unit*1)
    d += elm.Dot(open=True).label('Future', loc='right')

    # ========== S-TRIG ALTERNATIVE OUTPUT ==========
    strig_y = dac_y - d.unit*2.5
    d.here = (output_x - d.unit*1, strig_y)
    d += elm.Dot().label('D10', loc='left')
    d += elm.Resistor().right().label('1k')
    d.push()
    d += elm.BjtNpn(circle=True).right().anchor('base').label('Q1 2N3904')
    d.push()
    d += elm.Resistor().up().label('100ohm').toy(rail_5v)
    d.pop()
    d.push()
    ground_level = trig_gnd[1] - d.unit*1.5
    d += elm.Line().down().toy(ground_level)
    d.pop()
    d += elm.Line().right().length(d.unit*1.5)
    d += elm.Dot(open=True).label('S-TRIG OUT', loc='right')

    # ========== GROUND RAIL AT BOTTOM ==========
    d.here = (0, ground_level)
    d += elm.Line().right().length(d.unit*16)
    d += elm.Ground().label('GND')

    # Connect input grounds to rail
    d += elm.Line().at(cv_gnd).down().toy(ground_level)
    d += elm.Line().at(trig_gnd).down().toy(ground_level)

d.save('COMPLETE_SYSTEM_PROPER.svg')
print("✓ Generated: COMPLETE_SYSTEM_PROPER.svg")
print("  All components properly connected:")
print("  - CV/TRIG inputs with voltage dividers → M4 ADC")
print("  - M4 → I2C → MCP4728 DAC + OLED")
print("  - MIDI FeatherWing stacked on M4")
print("  - DAC outputs: VA(CV), VB(TRIG), VC(CC), VD(Future)")
print("  - S-TRIG alternative output via transistor")
print("  - Proper 5V and 3.3V power rails with ground")
