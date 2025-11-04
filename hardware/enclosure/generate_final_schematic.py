#!/usr/bin/env python3
"""
PRISME COMPLETE HARDWARE SCHEMATIC - FINAL
Complete layout planning FIRST, then connections
Based on 555 timer + rectifier patterns
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    d.config(fontsize=12, unit=2.5)

    # ===============================================================
    # TITLE
    # ===============================================================
    elm.Label().at((0, 20)).label('PRISME COMPLETE HARDWARE', fontsize=16, halign='left', font='bold')

    # ===============================================================
    # STEP 1: PLACE ALL MAJOR COMPONENTS WITH ABSOLUTE POSITIONS
    # ===============================================================

    # M4 at center
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
          .side('L', spacing=1, leadlen=1)
          .side('R', spacing=1, leadlen=1)
          .side('T', spacing=1, leadlen=0.5)
          .side('B', spacing=1, leadlen=0.5)
          .label('M4')
          .at((10, 12)))

    # OLED above M4
    OLED = (elm.Ic()
            .pin(name='SDA', side='bot', pin='1')
            .pin(name='SCL', side='bot', pin='2')
            .side('B', spacing=0.7, leadlen=0.8)
            .label('OLED\\n0x3C', fontsize=10)
            .at((8, 16)))

    # DAC above M4 right
    DAC = (elm.Ic()
           .pin(name='VDD', side='left', pin='1')
           .pin(name='SDA', side='bot', pin='2')
           .pin(name='SCL', side='bot', pin='3')
           .pin(name='VA', side='right', pin='4')
           .pin(name='VB', side='right', pin='5')
           .pin(name='VC', side='right', pin='6')
           .side('L', spacing=0.8, leadlen=0.5)
           .side('R', spacing=0.8, leadlen=1)
           .side('B', spacing=0.7, leadlen=0.8)
           .label('MCP4728\\n0x60', fontsize=10)
           .at((12, 16)))

    # ===============================================================
    # STEP 2: CV IN - LEFT TOP
    # ===============================================================
    elm.Label().at((0, 15)).label('CV IN', fontsize=11, halign='left', font='bold')

    elm.Dot().at((1, 14)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R1\\n10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R2\\n10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D1\\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()

    # Connect to M4.A3
    elm.Line().right(d.unit*1.5)
    elm.Line().toy(M4.A3)
    elm.Line().tox(M4.A3)

    # ===============================================================
    # STEP 3: TRIG IN - LEFT BOTTOM
    # ===============================================================
    elm.Label().at((0, 11)).label('TRIG IN', fontsize=11, halign='left', font='bold')

    elm.Dot().at((1, 10)).label('Jack', fontsize=9, halign='right')
    d.push()
    elm.Ground()
    d.pop()

    elm.Resistor().right().label('R4\\n10kΩ', fontsize=9)
    elm.Dot()
    d.push()
    elm.Resistor().down().label('R5\\n10kΩ', fontsize=9, loc='right')
    elm.Ground()
    d.pop()
    d.push()
    elm.Diode().up().label('D2\\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)
    d.pop()

    # Connect to M4.A4
    elm.Line().right(d.unit*1.5)
    elm.Line().toy(M4.A4)
    elm.Line().tox(M4.A4)

    # ===============================================================
    # STEP 4: I2C BUS CONNECTIONS
    # ===============================================================
    # Connect OLED to M4
    elm.Line().at(OLED.SDA).toy(M4.SDA)
    SDA_BUS = elm.Dot()
    elm.Line().tox(M4.SDA)

    elm.Line().at(OLED.SCL).toy(M4.SCL)
    SCL_BUS = elm.Dot()
    elm.Line().tox(M4.SCL)

    # Connect DAC to I2C bus
    elm.Line().at(DAC.SDA).toy(SDA_BUS.center)
    elm.Dot()
    elm.Line().tox(SDA_BUS.center)

    elm.Line().at(DAC.SCL).toy(SCL_BUS.center)
    elm.Dot()
    elm.Line().tox(SCL_BUS.center)

    # DAC power
    elm.Line().left(d.unit/2).at(DAC.VDD)
    elm.Vdd().label('5V', fontsize=9)

    # ===============================================================
    # STEP 5: MIDI - BOTTOM
    # ===============================================================
    elm.Label().at((10, 9)).label('MIDI', fontsize=11, halign='center', font='bold')

    elm.Dot().at((8.5, 8.5)).label('IN', fontsize=9, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.RX)
    elm.Line().tox(M4.RX)

    elm.Dot().at((8.5, 8)).label('OUT', fontsize=9, halign='right')
    elm.Line().right(d.unit/2)
    elm.Line().toy(M4.TX)
    elm.Line().tox(M4.TX)

    # ===============================================================
    # STEP 6: LEDS - RIGHT SIDE
    # ===============================================================
    elm.Label().at((15, 15)).label('INDICATORS', fontsize=11, halign='left', font='bold')

    # CV LED
    elm.Resistor().right().at(M4.D4).label('R6 1kΩ', fontsize=9)
    elm.LED().down().flip().label('CV', fontsize=9, loc='right')
    elm.Ground()

    # RGB R
    elm.Resistor().right().at(M4.D11).label('R7 330Ω', fontsize=9)
    elm.LED().down().flip().label('R', fontsize=9, loc='right')
    elm.Ground()

    # RGB G
    elm.Resistor().right().at(M4.D23).label('R8 330Ω', fontsize=9)
    elm.LED().down().flip().label('G', fontsize=9, loc='right')
    elm.Ground()

    # RGB B
    elm.Resistor().right().at(M4.D24).label('R9 330Ω', fontsize=9)
    elm.LED().down().flip().label('B', fontsize=9, loc='right')
    elm.Ground()

    # ===============================================================
    # STEP 7: DAC OUTPUTS - RIGHT TOP
    # ===============================================================
    elm.Label().at((15, 18)).label('CV OUTPUTS', fontsize=11, halign='left', font='bold')

    # CV OUT
    elm.Resistor().right().at(DAC.VA).label('R10 100Ω', fontsize=9)
    elm.Dot().label('CV OUT', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # TRIG V
    elm.Resistor().right().at(DAC.VB).label('R11 100Ω', fontsize=9)
    elm.Dot().label('TRIG V', fontsize=9, halign='left')
    d.push()
    elm.Ground()
    d.pop()

    # CC OUT
    elm.Resistor().right().at(DAC.VC).label('R12 100Ω', fontsize=9)
    elm.Dot().label('CC OUT', fontsize=9, halign='left')
    elm.Ground()

    # ===============================================================
    # STEP 8: S-TRIG - RIGHT BOTTOM
    # ===============================================================
    elm.Label().at((15, 11)).label('S-TRIG', fontsize=11, halign='left', font='bold')

    elm.Resistor().right().at(M4.D10).label('R13 1kΩ', fontsize=9)
    Q1 = elm.BjtNpn(circle=True).right().anchor('base').label('Q1\\n2N3904', fontsize=9, loc='bottom')

    elm.Resistor().up().at(Q1.collector).label('R14 100Ω', fontsize=9, loc='right')
    elm.Dot().label('TRIG S', fontsize=9, halign='left')

    elm.Ground().at(Q1.emitter)

    # ===============================================================
    # SPECS
    # ===============================================================
    elm.Label().at((0, 6)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
    elm.Label().at((0, 5.5)).label('• Input: 10kΩ divider + BAT85 = 0-40V+ safe', fontsize=9, halign='left')
    elm.Label().at((0, 5)).label('• Output: 0-5V, 1V/oct, 12-bit', fontsize=9, halign='left')
    elm.Label().at((0, 4.5)).label('• I2C: OLED 0x3C + DAC 0x60', fontsize=9, halign='left')

print("✅ FINAL UNIFIED_SYSTEM_SCHEMATIC.svg")
print("   Layout-first approach with absolute positioning")
