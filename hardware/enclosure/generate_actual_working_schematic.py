#!/usr/bin/env python3
"""
PRISME SCHEMATIC - ACTUALLY ROUTING THE RIGHT SIDE PROPERLY
Route DOWN first, then RIGHT to avoid crossing
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=12, unit=3, inches_per_unit=0.5)

    # Title
    elm.Label().at((0, 24)).label('PRISME HARDWARE SCHEMATIC', fontsize=16, halign='left', font='bold')

    # =======================================================================
    # CV IN
    # =======================================================================
    elm.Label().at((0, 22)).label('CV IN', fontsize=11, halign='left', font='bold')
    elm.Dot().at((1, 20)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()
    elm.Resistor().right().label('R1 10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R2 10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D1 BAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()
    elm.Line().right(d.unit*2)
    CV_TO_M4 = d.here

    # =======================================================================
    # TRIG IN
    # =======================================================================
    elm.Label().at((0, 17)).label('TRIG IN', fontsize=11, halign='left', font='bold')
    elm.Dot().at((1, 15)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()
    elm.Resistor().right().label('R4 10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R5 10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D2 BAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()
    elm.Line().right(d.unit*2)
    TRIG_TO_M4 = d.here

    # =======================================================================
    # M4
    # =======================================================================
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
          .side('L', spacing=1.5, pad=2, leadlen=1)
          .side('R', spacing=1.2, pad=2, leadlen=1.5)
          .side('T', spacing=2, pad=1, leadlen=1)
          .side('B', spacing=2, pad=1, leadlen=1)
          .label('M4', fontsize=11)
          .at((10, 16)))

    elm.Line().at(CV_TO_M4).toy(M4.A3)
    elm.Line().tox(M4.A3)
    elm.Line().at(TRIG_TO_M4).toy(M4.A4)
    elm.Line().tox(M4.A4)

    # =======================================================================
    # OLED
    # =======================================================================
    OLED = (elm.Ic()
            .pin(name='SDA', side='bot', pin='1')
            .pin(name='SCL', side='bot', pin='2')
            .side('B', spacing=1.2, leadlen=1.2)
            .label('OLED\n0x3C', fontsize=10)
            .at((7, 21)))

    elm.Line().at(OLED.SDA).toy(M4.SDA)
    SDA_J = elm.Dot()
    elm.Line().tox(M4.SDA)
    elm.Line().at(OLED.SCL).toy(M4.SCL)
    SCL_J = elm.Dot()
    elm.Line().tox(M4.SCL)

    # =======================================================================
    # DAC
    # =======================================================================
    DAC = (elm.Ic()
           .pin(name='VDD', side='left', pin='1')
           .pin(name='SDA', side='bot', pin='2')
           .pin(name='SCL', side='bot', pin='3')
           .pin(name='VA', side='right', pin='4')
           .pin(name='VB', side='right', pin='5')
           .pin(name='VC', side='right', pin='6')
           .side('L', spacing=1, leadlen=0.5)
           .side('R', spacing=1, leadlen=1.5)
           .side('B', spacing=1.2, leadlen=1.2)
           .label('DAC\n0x60', fontsize=10)
           .at((13, 21)))

    elm.Line().left(d.unit/3).at(DAC.VDD)
    elm.Vdd().label('5V', fontsize=9)
    elm.Line().at(DAC.SDA).toy(SDA_J.center)
    elm.Dot()
    elm.Line().tox(SDA_J.center)
    elm.Line().at(DAC.SCL).toy(SCL_J.center)
    elm.Dot()
    elm.Line().tox(SCL_J.center)

    # =======================================================================
    # MIDI
    # =======================================================================
    elm.Label().at((10, 12)).label('MIDI', fontsize=11, halign='center', font='bold')
    elm.Dot().at((8, 11.2)).label('IN', fontsize=9, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.RX)
    elm.Line().tox(M4.RX)
    elm.Dot().at((8, 10.6)).label('OUT', fontsize=9, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.TX)
    elm.Line().tox(M4.TX)

    # =======================================================================
    # RIGHT SIDE - ROUTE DOWN FIRST TO SEPARATE LEVELS
    # =======================================================================

    # DAC OUTPUTS at top
    elm.Label().at((16, 22.5)).label('CV OUTPUTS', fontsize=11, halign='left', font='bold')
    elm.Resistor().right().at(DAC.VA).label('R10 100Ω', fontsize=9)
    elm.Dot().label('CV OUT', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().at(DAC.VB).label('R11 100Ω', fontsize=9)
    elm.Dot().label('TRIG V', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().at(DAC.VC).label('R12 100Ω', fontsize=9)
    elm.Dot().label('CC OUT', fontsize=9, halign='left')
    elm.Ground()

    # CV LED - Route from D4 down to level 19, then right
    elm.Label().at((16, 19.5)).label('INDICATORS', fontsize=11, halign='left', font='bold')
    elm.Line().right(d.unit*0.3).at(M4.D4)
    elm.Line().down(d.unit*0.8)  # Go down to y=19
    elm.Line().right(d.unit*0.7)
    elm.Resistor().right().label('R6 1kΩ', fontsize=9)
    elm.LED().down().flip().label('CV', fontsize=9, loc='right')
    elm.Ground()

    # RGB R - Route from D11 down to level 17, then right
    elm.Line().right(d.unit*0.3).at(M4.D11)
    elm.Line().down(d.unit*0.8)  # Go down to y=17
    elm.Line().right(d.unit*0.7)
    elm.Resistor().right().label('R7 330Ω', fontsize=9)
    elm.LED().down().flip().label('R', fontsize=9, loc='right')
    elm.Ground()

    # RGB G - Route from D23 down to level 15, then right
    elm.Line().right(d.unit*0.3).at(M4.D23)
    elm.Line().down(d.unit*0.8)  # Go down to y=15
    elm.Line().right(d.unit*0.7)
    elm.Resistor().right().label('R8 330Ω', fontsize=9)
    elm.LED().down().flip().label('G', fontsize=9, loc='right')
    elm.Ground()

    # RGB B - Route from D24 down to level 13, then right
    elm.Line().right(d.unit*0.3).at(M4.D24)
    elm.Line().down(d.unit*0.8)  # Go down to y=13
    elm.Line().right(d.unit*0.7)
    elm.Resistor().right().label('R9 330Ω', fontsize=9)
    elm.LED().down().flip().label('B', fontsize=9, loc='right')
    elm.Ground()

    # S-TRIG - Route from D10
    elm.Label().at((16, 11)).label('S-TRIG', fontsize=11, halign='left', font='bold')
    elm.Line().right(d.unit*0.3).at(M4.D10)
    elm.Line().down(d.unit*0.5)  # Go down slightly
    elm.Line().right(d.unit*0.7)
    elm.Resistor().right().label('R13 1kΩ', fontsize=9)
    Q1 = elm.BjtNpn(circle=True).right().anchor('base').label('Q1\n2N3904', fontsize=9, loc='bottom')
    elm.Resistor().up().at(Q1.collector).label('R14 100Ω', fontsize=9, loc='right')
    elm.Dot().label('TRIG S', fontsize=9, halign='left')
    elm.Ground().at(Q1.emitter)

    # Specs
    elm.Label().at((0, 8)).label('SPECS:', fontsize=11, halign='left', font='bold')
    elm.Label().at((0, 7.5)).label('• Input: 10kΩ + BAT85 = 0-40V+ safe', fontsize=9, halign='left')
    elm.Label().at((0, 7)).label('• Output: 0-5V, 1V/oct, 12-bit', fontsize=9, halign='left')

print("✅ SCHEMATIC WITH PROPER DOWN-THEN-RIGHT ROUTING")
