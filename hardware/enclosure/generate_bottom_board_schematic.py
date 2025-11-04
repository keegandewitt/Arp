#!/usr/bin/env python3
"""
PRISME BOTTOM BOARD (OUTPUT BOARD) - Complete Production Schematic
Includes: USB-C breakout, MCP4728 DAC, CV/Gate/CC outputs, MIDI LEDs, S-Trig circuit
"""

import schemdraw
import schemdraw.elements as elm

def generate_bottom_board_schematic():
    """Generate complete schematic for BOTTOM (OUTPUT) board"""

    dwg = schemdraw.Drawing(fontsize=12)

    # ==================== TITLE ====================
    dwg += elm.Label().label('PRISME BOTTOM BOARD (OUTPUT BOARD) - Complete Schematic', fontsize=20)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Board: 90mm x 55mm custom-cut ElectroCookie protoboard | Position: Bottom layer', fontsize=10)
    dwg += elm.Gap().down(4)

    # ==================== USB-C SECTION ====================
    dwg += elm.Label().label('------ USB-C PANEL MOUNT BREAKOUT ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Position: Rear panel, 8mm from left edge | 9.5mm x 3.8mm cutout', fontsize=10)
    dwg += elm.Gap().down(1)

    dwg.push()
    dwg += elm.Label().label('+──────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  USB-C Panel Breakout   |', fontsize=11)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  (Extension to M4 USB)  |', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('+──────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('    DOWN USB-C Extension Cable', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('    DOWN To Feather M4 USB port', fontsize=9)

    dwg.pop()
    dwg += elm.Gap().down(8)

    # ==================== MCP4728 DAC SECTION ====================
    dwg += elm.Label().label('------ MCP4728 4-CHANNEL DAC MODULE ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('I2C Address: 0x60 | 12-bit resolution | 0-5V output range', fontsize=10)
    dwg += elm.Gap().down(1)

    dwg.push()
    dwg += elm.Label().label('+────────────────────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|         MCP4728 DAC Module            |', fontsize=11)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  Power: VDD(5V), GND                  |', fontsize=9)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('|  I2C: SDA(D21), SCL(D22) from M4      |', fontsize=9)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('|  Decoupling: C3(0.1uF), C4(0.1uF)     |', fontsize=9)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  CH_A  |  CH_B  |  CH_C  |  CH_D      |', fontsize=10)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('|  CV    |  TRIG  |  CC    |  (Future)  |', fontsize=9)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('+────────────────────────────────────────+', fontsize=10)

    dwg.pop()
    dwg += elm.Gap().down(12)

    # ==================== POWER SECTION ====================
    dwg += elm.Label().label('------ POWER DISTRIBUTION ------', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Label().label('5V Rail (from headers):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('5V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C1 47uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2.5)
    dwg += elm.Dot().label('5V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C2 0.1uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('3.3V Rail (from headers):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C9 10uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C10 0.1uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== CV OUTPUT ====================
    dwg += elm.Label().label('------ CV OUTPUT (MCP4728 Channel A -> Rear Jack 20mm) ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Purpose: 1V/octave pitch control | 0-5V = 5 octaves (MIDI 0-60, C0-C4)', fontsize=10)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Dot().label('CH_A\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R1 100ohm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    cv_node_x = dwg.here[0]
    cv_node_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (cv_node_x - 0.6, cv_node_y - 1.5)
    dwg += elm.Label().label('C6\n100nF', fontsize=10)

    dwg.here = (cv_node_x, cv_node_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('CV OUT\nJack', loc='right', fontsize=12)

    # CV LED
    dwg.pop()
    dwg += elm.Gap().down(8)
    dwg += elm.Label().label('CV Activity LED (rear panel, 27mm from left):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D12', loc='left', fontsize=11)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R7 150ohm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White 3mm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== TRIG OUTPUT ====================
    dwg += elm.Label().label('------ TRIG OUTPUT - DUAL MODE (Rear Jack 32mm) ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('V-Trig: MCP4728 Channel B direct (0V/5V) | S-Trig: GPIO D10 via NPN transistor (open/GND)', fontsize=10)
    dwg += elm.Gap().down(2)

    # V-Trig path
    dwg.push()
    dwg += elm.Label().label('V-Trig Mode (D10=LOW):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('CH_B\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R2 100ohm', loc='top', fontsize=11)
    dwg += elm.Line().right(4)
    dwg += elm.Dot().label('TRIG OUT\nJack', loc='right', fontsize=12)

    # S-Trig path
    dwg.pop()
    dwg += elm.Gap().down(5)
    dwg += elm.Label().label('S-Trig Mode (D10=HIGH):', fontsize=11)
    dwg += elm.Gap().down(0.5)

    dwg.push()
    dwg += elm.Dot().label('D10\nGPIO', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R5 1kohm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.BjtNpn().right().anchor('base').label('Q1\n2N3904', loc='bottom', fontsize=10)

    npn_x = dwg.here[0]
    npn_y = dwg.here[1]

    # Collector to output
    dwg.here = (npn_x + 0.5, npn_y + 0.8)
    dwg += elm.Line().up(0.5)
    dwg += elm.Resistor().right().label('R6 100ohm', loc='top', fontsize=10)
    dwg += elm.Line().up(2)
    dwg += elm.Dot().label('UP to jack', loc='right', fontsize=9)

    # Emitter to ground
    dwg.here = (npn_x + 0.5, npn_y - 0.8)
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # TRIG RGB LED
    dwg.pop()
    dwg += elm.Gap().down(9)
    dwg += elm.Label().label('TRIG Mode/Activity RGB LED (rear panel, 39mm from left):', fontsize=11)
    dwg += elm.Gap().down(0.5)

    dwg.push()
    dwg += elm.Dot().label('A0 (RED)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R11 150ohm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('RED', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2)
    dwg += elm.Dot().label('A1 (GRN)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R12 150ohm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('GREEN', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(4)
    dwg += elm.Dot().label('A2 (BLU)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R13 150ohm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('BLUE', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== CC OUTPUT ====================
    dwg += elm.Label().label('------ CC OUTPUT (MCP4728 Channel C -> Rear Jack 44mm) ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Purpose: Custom CC mapping with Learn Mode | 0-5V modulation output', fontsize=10)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Dot().label('CH_C\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R3 100ohm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    cc_node_x = dwg.here[0]
    cc_node_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (cc_node_x - 0.6, cc_node_y - 1.5)
    dwg += elm.Label().label('C7\n100nF', fontsize=10)

    dwg.here = (cc_node_x, cc_node_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('CC OUT\nJack', loc='right', fontsize=12)

    # CC LED
    dwg.pop()
    dwg += elm.Gap().down(8)
    dwg += elm.Label().label('CC Activity LED (rear panel, 51mm from left):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D25', loc='left', fontsize=11)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R8 150ohm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White 3mm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== MIDI LEDS ====================
    dwg += elm.Label().label('------ MIDI ACTIVITY INDICATORS ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('MIDI OUT jack at 65mm | MIDI IN jack at 85mm from left edge', fontsize=10)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Label().label('MIDI OUT TX Activity (72mm from left):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('CAN_TX', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R9 150ohm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White 3mm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('MIDI IN RX Activity (92mm from left):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('A5', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R10 150ohm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White 3mm', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    # ==================== NOTES ====================
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('NOTES:', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• MCP4728 I2C address 0x60, shared bus with OLED (0x3C)', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• All DAC outputs: 100ohm series resistor for short-circuit protection', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• CV & CC: 100nF low-pass filter for noise reduction', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• TRIG: No filter cap on V-Trig path to preserve fast gate edges', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• S-Trig: NPN transistor pulls output to GND (open when idle, short when triggered)', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• RGB LED: GREEN = V-Trig mode | RED = S-Trig mode | Brightness = activity', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• All LEDs: 150ohm current limiting resistors (3.3V logic, ~10mA per LED)', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• Power decoupling: C1/C2 (5V rail), C9/C10 (3.3V rail), C3/C4 (DAC)', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• USB-C provides power + USB MIDI communication to Feather M4', fontsize=9)

    # Save
    dwg.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_BOARD_SCHEMATIC.svg')

    print("✅ Bottom board schematic generated (complete with USB-C and MCP4728)")
    return dwg


if __name__ == "__main__":
    generate_bottom_board_schematic()
