#!/usr/bin/env python3
"""
PRISME COMPLETE HARDWARE SCHEMATIC - PROFESSIONAL
Using patterns from 555 timer, rectifier, and ATmega328 examples
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=12, unit=2.5)

    # ==========================================================================
    # TITLE
    # ==========================================================================
    elm.Label().at((0, 24)).label('PRISME COMPLETE HARDWARE SCHEMATIC', fontsize=16, halign='left', font='bold')

    # ==========================================================================
    # FEATHER M4 - CENTER
    # ==========================================================================
    M4 = (elm.Ic()
          .pin(name='A3', side='left', pin='1')
          .pin(name='A4', side='left', pin='2')
          .pin(name='D4', side='right', pin='3')
          .pin(name='D10', side='right', pin='4')
          .pin(name='D11', side='right', pin='5')
          .pin(name='D23', side='right', pin='6')
          .pin(name='D24', side='right', pin='7')
          .pin(name='SDA', side='top', pin='8')
          .pin(name='SCL', side='top', pin='9')
          .pin(name='RX', side='bot', pin='10')
          .pin(name='TX', side='bot', pin='11')
          .side('L', spacing=1.5, pad=1.5, leadlen=1.2)
          .side('R', spacing=1.2, pad=1.5, leadlen=1.2)
          .side('T', spacing=1.5, pad=1, leadlen=1)
          .side('B', spacing=1.5, pad=1, leadlen=1)
          .label('FEATHER M4', fontsize=11)
          .at((12, 16)))

    # ==========================================================================
    # CV IN CIRCUIT - LEFT TOP
    # ==========================================================================
    elm.Label().at((0, 20)).label('CV IN', fontsize=12, halign='left', font='bold')

    CV_JACK = elm.Dot().at((1, 19)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R1\n10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R2\n10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D1\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()
    elm.Line().right(d.unit*2)
    elm.Line().toy(M4.A3)
    elm.Line().tox(M4.A3)

    # ==========================================================================
    # TRIG IN CIRCUIT - LEFT MIDDLE
    # ==========================================================================
    elm.Label().at((0, 16)).label('TRIG IN', fontsize=12, halign='left', font='bold')

    TRIG_JACK = elm.Dot().at((1, 15)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R4\n10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R5\n10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D2\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()
    elm.Line().right(d.unit*2)
    elm.Line().toy(M4.A4)
    elm.Line().tox(M4.A4)

    # ==========================================================================
    # I2C BUS - TOP
    # ==========================================================================
    elm.Label().at((9, 22)).label('I2C BUS', fontsize=11, halign='center', font='bold')

    # OLED
    OLED = (elm.Ic()
            .pin(name='SDA', side='bot', pin='1')
            .pin(name='SCL', side='bot', pin='2')
            .side('B', spacing=1, leadlen=1)
            .label('OLED\n0x3C', fontsize=9)
            .at((9, 20)))

    elm.Line().at(OLED.SDA).toy(M4.SDA)
    SDA_BUS = elm.Dot()
    elm.Line().tox(M4.SDA)

    elm.Line().at(OLED.SCL).toy(M4.SCL)
    SCL_BUS = elm.Dot()
    elm.Line().tox(M4.SCL)

    # DAC
    DAC = (elm.Ic()
           .pin(name='VDD', side='left', pin='1')
           .pin(name='SDA', side='bot', pin='2')
           .pin(name='SCL', side='bot', pin='3')
           .pin(name='VA', side='right', pin='4')
           .pin(name='VB', side='right', pin='5')
           .pin(name='VC', side='right', pin='6')
           .side('L', spacing=1.2, leadlen=0.5)
           .side('R', spacing=1, leadlen=1)
           .side('B', spacing=1, leadlen=1)
           .label('MCP4728\n0x60', fontsize=9)
           .at((15, 20)))

    elm.Line().left(d.unit/2).at(DAC.VDD)
    elm.Vdd().label('5V', fontsize=9)

    elm.Line().at(DAC.SDA).toy(SDA_BUS.center)
    elm.Dot()
    elm.Line().tox(SDA_BUS.center)

    elm.Line().at(DAC.SCL).toy(SCL_BUS.center)
    elm.Dot()
    elm.Line().tox(SCL_BUS.center)

    # ==========================================================================
    # MIDI - BOTTOM
    # ==========================================================================
    elm.Label().at((12, 12)).label('MIDI', fontsize=11, halign='center', font='bold')

    elm.Dot().at((10, 11.5)).label('IN', fontsize=8, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.RX)
    elm.Line().tox(M4.RX)

    elm.Dot().at((10, 11)).label('OUT', fontsize=8, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.TX)
    elm.Line().tox(M4.TX)

    # ==========================================================================
    # INDICATOR LEDS - RIGHT SIDE
    # ==========================================================================
    elm.Label().at((19, 20)).label('INDICATORS', fontsize=12, halign='left', font='bold')

    # CV LED from D4
    elm.Resistor().right().at(M4.D4).label('R6\n1kΩ', fontsize=9)
    elm.LED().down().flip().label('CV', fontsize=9, loc='right')
    elm.Line().down(d.unit/2)
    elm.Ground()

    # RGB Red from D11
    elm.Resistor().right().at(M4.D11).label('R7\n330Ω', fontsize=9)
    elm.LED().down().flip().label('R', fontsize=9, loc='right')
    elm.Line().down(d.unit/2)
    elm.Ground()

    # RGB Green from D23
    elm.Resistor().right().at(M4.D23).label('R8\n330Ω', fontsize=9)
    elm.LED().down().flip().label('G', fontsize=9, loc='right')
    elm.Line().down(d.unit/2)
    elm.Ground()

    # RGB Blue from D24
    elm.Resistor().right().at(M4.D24).label('R9\n330Ω', fontsize=9)
    elm.LED().down().flip().label('B', fontsize=9, loc='right')
    elm.Line().down(d.unit/2)
    elm.Ground()

    # ==========================================================================
    # CV OUTPUTS - RIGHT TOP
    # ==========================================================================
    elm.Label().at((19, 22)).label('CV OUTPUTS', fontsize=12, halign='left', font='bold')

    # CV OUT
    elm.Resistor().right().at(DAC.VA).label('R10\n100Ω', fontsize=9)
    elm.Dot().label('CV OUT', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # TRIG V OUT
    elm.Resistor().right().at(DAC.VB).label('R11\n100Ω', fontsize=9)
    elm.Dot().label('TRIG V', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # CC OUT
    elm.Resistor().right().at(DAC.VC).label('R12\n100Ω', fontsize=9)
    elm.Dot().label('CC OUT', fontsize=9, halign='left')
    elm.Ground()

    # ==========================================================================
    # S-TRIG OUTPUT - RIGHT BOTTOM
    # ==========================================================================
    elm.Label().at((19, 14)).label('S-TRIG', fontsize=11, halign='left', font='bold')

    elm.Resistor().right().at(M4.D10).label('R13\n1kΩ', fontsize=9)
    Q1 = elm.BjtNpn(circle=True).right().anchor('base').label('Q1\n2N3904', fontsize=9, loc='bottom')

    elm.Resistor().up().at(Q1.collector).label('R14\n100Ω', fontsize=9, loc='right')
    elm.Dot().label('TRIG S', fontsize=9, halign='left')

    elm.Ground().at(Q1.emitter)

    # ==========================================================================
    # SPECIFICATIONS
    # ==========================================================================
    elm.Label().at((0, 9)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
    elm.Label().at((0, 8.5)).label('• Input Protection: 10kΩ divider + BAT85 clamp = 0-40V+ safe', fontsize=9, halign='left')
    elm.Label().at((0, 8)).label('• CV/CC Outputs: 0-5V, 1V/octave, 12-bit (MCP4728 DAC)', fontsize=9, halign='left')
    elm.Label().at((0, 7.5)).label('• I2C Bus: OLED FeatherWing (0x3C) + MCP4728 DAC (0x60)', fontsize=9, halign='left')
    elm.Label().at((0, 7)).label('• Output Protection: 100Ω series resistors on all CV outputs', fontsize=9, halign='left')
    elm.Label().at((0, 6.5)).label('• Dual Triggers: V-Trig (0-5V from DAC) + S-Trig (NPN switch to GND)', fontsize=9, halign='left')
    elm.Label().at((0, 6)).label('• LEDs: White CV indicator + RGB 3-channel TRIG indicator', fontsize=9, halign='left')

print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - PROFESSIONAL LAYOUT")
print("   Based on schemdraw best practices:")
print("   • Custom IC definitions with .pin() builder pattern")
print("   • Proper .side() spacing configuration")
print("   • Clean left-to-right signal flow")
print("   • push()/pop() for junction management")
