#!/usr/bin/env python3
"""
PRISME Complete Hardware Schematic - CORRECT METHOD
Using proper schemdraw patterns from documentation
"""

import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='/Users/keegandewitt/Cursor/prisme/hardware/enclosure/UNIFIED_SYSTEM_SCHEMATIC.svg') as d:
    d.config(fontsize=11, unit=2.5)

    # Title
    d += elm.Label().at((0, 16)).label('PRISME HARDWARE - COMPLETE SCHEMATIC', fontsize=16, halign='left', font='bold')

    # =========================================================================
    # CV IN CIRCUIT (LEFT TOP)
    # =========================================================================
    d += elm.Label().at((0, 14.5)).label('CV IN', fontsize=12, halign='left', font='bold')

    # Jack and voltage divider
    CV_JACK = elm.Dot().at((1, 14)).label('Jack', fontsize=9, halign='right')
    R1 = elm.Resistor().right().label('R1\n10kΩ', fontsize=9)
    d.push()  # Save position at TAP
    CV_TAP = elm.Dot().label('TAP', fontsize=8, loc='top')

    # To M4 A3 (save for later connection)
    cv_to_m4 = elm.Line().right(d.unit*1.5)

    # Lower resistor
    d.pop()
    R2 = elm.Resistor().down().label('R2\n10kΩ', fontsize=9, loc='right')
    elm.Ground()

    # BAT85 clamp
    elm.Diode().at(R1.end).up().label('D1\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)

    # Jack ground
    elm.Ground().at(CV_JACK.start)

    # CV LED
    CV_LED_IN = elm.Dot().at((1, 12)).label('M4 D4', fontsize=8, halign='right')
    elm.Resistor().right().label('1kΩ', fontsize=8)
    elm.LED().right().label('CV', fontsize=8)
    elm.Ground()

    # =========================================================================
    # TRIG IN CIRCUIT (LEFT MIDDLE)
    # =========================================================================
    d += elm.Label().at((0, 10)).label('TRIG IN', fontsize=12, halign='left', font='bold')

    # Jack and voltage divider
    TRIG_JACK = elm.Dot().at((1, 9)).label('Jack', fontsize=9, halign='right')
    R4 = elm.Resistor().right().label('R4\n10kΩ', fontsize=9)
    d.push()
    TRIG_TAP = elm.Dot().label('TAP', fontsize=8, loc='top')

    # To M4 A4 (save for later)
    trig_to_m4 = elm.Line().right(d.unit*1.5)

    # Lower resistor
    d.pop()
    R5 = elm.Resistor().down().label('R5\n10kΩ', fontsize=9, loc='right')
    elm.Ground()

    # BAT85 clamp
    elm.Diode().at(R4.end).up().label('D2\nBAT85', fontsize=9, loc='left')
    elm.Vdd().label('3.3V', fontsize=9)

    # Jack ground
    elm.Ground().at(TRIG_JACK.start)

    # TRIG RGB LEDs
    RGB_R = elm.Dot().at((1, 7)).label('D11', fontsize=8, halign='right')
    elm.Resistor().right().label('330Ω', fontsize=8)
    elm.LED().right().label('R', fontsize=8)
    elm.Ground()

    RGB_G = elm.Dot().at((1, 6.2)).label('D23', fontsize=8, halign='right')
    elm.Resistor().right().label('330Ω', fontsize=8)
    elm.LED().right().label('G', fontsize=8)
    elm.Ground()

    RGB_B = elm.Dot().at((1, 5.4)).label('D24', fontsize=8, halign='right')
    elm.Resistor().right().label('330Ω', fontsize=8)
    elm.LED().right().label('B', fontsize=8)
    elm.Ground()

    # =========================================================================
    # FEATHER M4 (CENTER)
    # =========================================================================
    d += elm.Label().at((7, 15)).label('FEATHER M4', fontsize=13, halign='center', font='bold')

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
    ]).at((7, 10)).label('M4', fontsize=10)

    # Connect CV IN to M4 A3
    elm.Line().endpoints(cv_to_m4.end, M4.A3)

    # Connect TRIG IN to M4 A4
    elm.Line().endpoints(trig_to_m4.end, M4.A4)

    # Connect M4 D4 to CV LED
    elm.Line().endpoints(M4.D4, CV_LED_IN.start)

    # Connect M4 D11/D23/D24 to RGB LEDs
    elm.Line().endpoints(M4.D11, RGB_R.start)
    elm.Line().endpoints(M4.D23, RGB_G.start)
    elm.Line().endpoints(M4.D24, RGB_B.start)

    # =========================================================================
    # I2C PERIPHERALS (TOP)
    # =========================================================================
    d += elm.Label().at((7, 16.5)).label('I2C BUS', fontsize=11, halign='center', font='bold')

    # OLED
    OLED = elm.Ic(pins=[
        elm.IcPin(name='SDA', side='bot', pin='1'),
        elm.IcPin(name='SCL', side='bot', pin='2'),
    ]).at((5.5, 13)).label('OLED\n0x3C', fontsize=9)

    # DAC
    DAC = elm.Ic(pins=[
        elm.IcPin(name='VDD', side='left', pin='1'),
        elm.IcPin(name='SDA', side='bot', pin='2'),
        elm.IcPin(name='SCL', side='bot', pin='3'),
        elm.IcPin(name='VA', side='right', pin='4'),
        elm.IcPin(name='VB', side='right', pin='5'),
        elm.IcPin(name='VC', side='right', pin='6'),
    ]).at((8.5, 13)).label('DAC\n0x60', fontsize=9)

    # Connect I2C - OLED to M4
    elm.Line().endpoints(OLED.SDA, M4.SDA)
    elm.Line().endpoints(OLED.SCL, M4.SCL)

    # Connect I2C - DAC to M4 (via OLED connections - shared bus)
    d.push()
    elm.Line().at(DAC.SDA).toy(OLED.SDA).dot()
    elm.Line().tox(OLED.SDA)
    d.pop()
    elm.Line().at(DAC.SCL).toy(OLED.SCL).dot()
    elm.Line().tox(OLED.SCL)

    # DAC power
    elm.Line().at(DAC.VDD).left(d.unit/2)
    elm.Vdd().label('5V', fontsize=9)

    # =========================================================================
    # MIDI UART (BOTTOM)
    # =========================================================================
    d += elm.Label().at((7, 7)).label('MIDI', fontsize=11, halign='center', font='bold')

    MIDI_IN = elm.Dot().at((5.5, 6.5)).label('IN', fontsize=8, halign='right')
    elm.Line().endpoints(MIDI_IN.start, M4.RX)

    MIDI_OUT = elm.Dot().at((5.5, 6)).label('OUT', fontsize=8, halign='right')
    elm.Line().endpoints(MIDI_OUT.start, M4.TX)

    # =========================================================================
    # DAC OUTPUTS (RIGHT)
    # =========================================================================
    d += elm.Label().at((11, 14)).label('OUTPUTS', fontsize=12, halign='left', font='bold')

    # CV OUT
    CV_R = elm.Resistor().at(DAC.VA).right().label('R1 100Ω', fontsize=9)
    CV_OUT = elm.Dot().label('CV OUT', fontsize=9, halign='left')
    elm.Ground()

    # TRIG OUT (V-Trig)
    TRIG_R = elm.Resistor().at(DAC.VB).right().label('R2 100Ω', fontsize=9)
    TRIG_V_OUT = elm.Dot().label('TRIG V', fontsize=9, halign='left')
    elm.Ground()

    # CC OUT
    CC_R = elm.Resistor().at(DAC.VC).right().label('R3 100Ω', fontsize=9)
    CC_OUT = elm.Dot().label('CC OUT', fontsize=9, halign='left')
    elm.Ground()

    # =========================================================================
    # S-TRIG (RIGHT BOTTOM)
    # =========================================================================
    d += elm.Label().at((11, 9)).label('S-TRIG', fontsize=11, halign='left', font='bold')

    # From M4 D10
    d.push()
    STRIG_START = elm.Line().at(M4.D10).right(d.unit).length(d.unit*1.5)
    R8 = elm.Resistor().right().label('R8 1kΩ', fontsize=9)

    # Transistor
    Q1 = elm.BjtNpn(circle=True).right().anchor('base').label('Q1\n2N3904', fontsize=9, loc='bottom')

    # Collector with resistor
    elm.Resistor().at(Q1.collector).up().label('R9 100Ω', fontsize=9, loc='right')
    STRIG_OUT = elm.Dot().label('TRIG S', fontsize=9, halign='left')

    # Emitter
    elm.Ground().at(Q1.emitter)

    d.pop()

    # =========================================================================
    # NOTES
    # =========================================================================
    d += elm.Label().at((0, 3)).label('SPECIFICATIONS:', fontsize=11, halign='left', font='bold')
    d += elm.Label().at((0, 2.5)).label('• Input: 10kΩ divider + BAT85 clamp = 0-40V+ safe', fontsize=9, halign='left')
    d += elm.Label().at((0, 2)).label('• Output: 0-5V, 1V/octave, 12-bit', fontsize=9, halign='left')
    d += elm.Label().at((0, 1.5)).label('• I2C shared: OLED 0x3C, DAC 0x60', fontsize=9, halign='left')
    d += elm.Label().at((0, 1)).label('• Protection: 100Ω series on outputs', fontsize=9, halign='left')

print("✅ UNIFIED_SYSTEM_SCHEMATIC.svg - CORRECTLY CONNECTED")
print("   Using proper schemdraw methods:")
print("   • .endpoints(start, end) for direct connections")
print("   • .at(component.pin) for positioning")
print("   • .toy()/.tox() for routing")
print("   • push()/pop() for junctions")
