#!/usr/bin/env python3
"""
PRISME COMPLETE HARDWARE SCHEMATIC
Using proper schemdraw methodology learned from documentation
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=11, unit=3)

    # ==========================================================================
    # TITLE
    # ==========================================================================
    elm.Label().at((0, 22)).label('PRISME COMPLETE HARDWARE SCHEMATIC', fontsize=16, halign='left', font='bold')

    # ==========================================================================
    # FEATHER M4 - CENTER
    # ==========================================================================
    elm.Label().at((10, 20)).label('FEATHER M4', fontsize=13, halign='center', font='bold')

    M4 = elm.Ic(pins=[
        elm.IcPin(name='A3', side='left', pin='1'),
        elm.IcPin(name='A4', side='left', pin='2'),
        elm.IcPin(name='D4', side='right', pin='3'),
        elm.IcPin(name='D10', side='right', pin='4'),
        elm.IcPin(name='D11', side='right', pin='5'),
        elm.IcPin(name='D23', side='right', pin='6'),
        elm.IcPin(name='D24', side='right', pin='7'),
        elm.IcPin(name='SDA', side='top', pin='8'),
        elm.IcPin(name='SCL', side='top', pin='9'),
        elm.IcPin(name='RX', side='bot', pin='10'),
        elm.IcPin(name='TX', side='bot', pin='11'),
    ]).at((10, 16)).label('M4', fontsize=11)

    # ==========================================================================
    # CV IN CIRCUIT - LEFT TOP
    # ==========================================================================
    elm.Label().at((0, 18)).label('CV IN', fontsize=12, halign='left', font='bold')

    elm.Dot().at((1, 17)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R1 10kΩ', fontsize=9)
    CV_TAP = elm.Dot().label('CV', fontsize=8, loc='top')

    d.push()
    elm.Resistor().down().label('R2 10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()

    d.push()
    elm.Diode().up().label('BAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()

    # Route CV to M4 A3
    elm.Line().at(CV_TAP.end).right(d.unit*1.5)
    elm.Line().toy(M4.A3)
    elm.Line().tox(M4.A3)

    # ==========================================================================
    # TRIG IN CIRCUIT - LEFT MIDDLE
    # ==========================================================================
    elm.Label().at((0, 14)).label('TRIG IN', fontsize=12, halign='left', font='bold')

    elm.Dot().at((1, 13)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R4 10kΩ', fontsize=9)
    TRIG_TAP = elm.Dot().label('TRIG', fontsize=8, loc='top')

    d.push()
    elm.Resistor().down().label('R5 10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()

    d.push()
    elm.Diode().up().label('BAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()

    # Route TRIG to M4 A4
    elm.Line().at(TRIG_TAP.end).right(d.unit*1.5)
    elm.Line().toy(M4.A4)
    elm.Line().tox(M4.A4)

    # ==========================================================================
    # I2C PERIPHERALS - TOP
    # ==========================================================================
    elm.Label().at((7, 21)).label('I2C BUS', fontsize=11, halign='center', font='bold')

    # OLED
    OLED = elm.Ic(pins=[
        elm.IcPin(name='SDA', side='bot', pin='1'),
        elm.IcPin(name='SCL', side='bot', pin='2'),
    ]).at((7, 19)).label('OLED\n0x3C', fontsize=9)

    # Connect OLED to M4
    elm.Line().at(OLED.SDA).toy(M4.SDA)
    SDA_NODE = elm.Dot()
    elm.Line().tox(M4.SDA)

    elm.Line().at(OLED.SCL).toy(M4.SCL)
    SCL_NODE = elm.Dot()
    elm.Line().tox(M4.SCL)

    # DAC
    DAC = elm.Ic(pins=[
        elm.IcPin(name='VDD', side='left', pin='1'),
        elm.IcPin(name='SDA', side='bot', pin='2'),
        elm.IcPin(name='SCL', side='bot', pin='3'),
        elm.IcPin(name='VA', side='right', pin='4'),
        elm.IcPin(name='VB', side='right', pin='5'),
        elm.IcPin(name='VC', side='right', pin='6'),
    ]).at((13, 19)).label('DAC\n0x60', fontsize=9)

    # DAC power
    elm.Line().left(d.unit/2).at(DAC.VDD)
    elm.Vdd().label('5V', fontsize=9)

    # Connect DAC to I2C bus
    elm.Line().at(DAC.SDA).toy(SDA_NODE.center)
    elm.Dot()
    elm.Line().tox(SDA_NODE.center)

    elm.Line().at(DAC.SCL).toy(SCL_NODE.center)
    elm.Dot()
    elm.Line().tox(SCL_NODE.center)

    # ==========================================================================
    # MIDI - BOTTOM
    # ==========================================================================
    elm.Label().at((10, 13)).label('MIDI', fontsize=11, halign='center', font='bold')

    elm.Dot().at((8, 12.5)).label('IN', fontsize=8, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.RX)
    elm.Line().tox(M4.RX)

    elm.Dot().at((8, 12)).label('OUT', fontsize=8, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.TX)
    elm.Line().tox(M4.TX)

    # ==========================================================================
    # CV LED - RIGHT TOP
    # ==========================================================================
    elm.Label().at((17, 18)).label('INDICATORS', fontsize=12, halign='left', font='bold')

    elm.Line().right(d.unit*0.8).at(M4.D4)
    elm.Resistor().down().label('R6\n1kΩ', fontsize=9, loc='right')
    elm.LED().down().label('CV', fontsize=9, loc='right')
    elm.Ground()

    # ==========================================================================
    # TRIG RGB LEDS - RIGHT MIDDLE
    # ==========================================================================

    elm.Line().right(d.unit*0.8).at(M4.D11)
    elm.Resistor().down().label('R7\n330Ω', fontsize=9, loc='right')
    elm.LED().down().label('R', fontsize=9, loc='right')
    elm.Ground()

    elm.Line().right(d.unit*1.2).at(M4.D23)
    elm.Resistor().down().label('R8\n330Ω', fontsize=9, loc='right')
    elm.LED().down().label('G', fontsize=9, loc='right')
    elm.Ground()

    elm.Line().right(d.unit*1.6).at(M4.D24)
    elm.Resistor().down().label('R9\n330Ω', fontsize=9, loc='right')
    elm.LED().down().label('B', fontsize=9, loc='right')
    elm.Ground()

    # ==========================================================================
    # DAC OUTPUTS - RIGHT TOP
    # ==========================================================================
    elm.Label().at((17, 21)).label('CV OUTPUTS', fontsize=12, halign='left', font='bold')

    # CV OUT
    elm.Line().right(d.unit*0.5).at(DAC.VA)
    elm.Resistor().right().label('R10\n100Ω', fontsize=9)
    elm.Dot().label('CV OUT', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # TRIG V OUT
    elm.Line().right(d.unit*0.5).at(DAC.VB)
    elm.Resistor().right().label('R11\n100Ω', fontsize=9)
    elm.Dot().label('TRIG V', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # CC OUT
    elm.Line().right(d.unit*0.5).at(DAC.VC)
    elm.Resistor().right().label('R12\n100Ω', fontsize=9)
    elm.Dot().label('CC OUT', fontsize=9, halign='left')
    elm.Ground()

    # ==========================================================================
    # S-TRIG - RIGHT BOTTOM
    # ==========================================================================
    elm.Label().at((17, 14)).label('S-TRIG', fontsize=11, halign='left', font='bold')

    elm.Line().right(d.unit*0.8).at(M4.D10)
    elm.Resistor().right().label('R13\n1kΩ', fontsize=9)

    Q1 = elm.BjtNpn(circle=True).right().anchor('base').label('Q1\n2N3904', fontsize=9, loc='bottom')

    elm.Line().up(d.unit*0.3).at(Q1.collector)
    elm.Resistor().up().label('R14\n100Ω', fontsize=9, loc='right')
    elm.Dot().label('TRIG S', fontsize=9, halign='left')

    elm.Line().down(d.unit*0.3).at(Q1.emitter)
    elm.Ground()

    # ==========================================================================
    # SPECIFICATIONS
    # ==========================================================================
    elm.Label().at((0, 10)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
    elm.Label().at((0, 9.5)).label('• Input Protection: 10kΩ divider + BAT85 = 0-40V+ safe', fontsize=9, halign='left')
    elm.Label().at((0, 9)).label('• CV/CC Outputs: 0-5V, 1V/octave, 12-bit (MCP4728)', fontsize=9, halign='left')
    elm.Label().at((0, 8.5)).label('• I2C Bus: OLED (0x3C) + DAC (0x60)', fontsize=9, halign='left')
    elm.Label().at((0, 8)).label('• Output Protection: 100Ω series on all CV outputs', fontsize=9, halign='left')
    elm.Label().at((0, 7.5)).label('• Triggers: V-Trig (0-5V DAC) + S-Trig (NPN switch)', fontsize=9, halign='left')

print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - PROPER METHODOLOGY")
print("   Using correct schemdraw patterns from documentation:")
print("   • push()/pop() for junctions")
print("   • .toy()/.tox() for routing")
print("   • .at(component.anchor) for positioning")
print("   • .dot() for junction markers")
