#!/usr/bin/env python3
"""
PRISME BOTTOM BOARD (OUTPUT BOARD) - Clean Schematic
Proper label positioning - labels to the SIDE of vertical components
"""

import schemdraw
import schemdraw.elements as elm

def generate_bottom_board_schematic():
    """Generate schematic for BOTTOM (OUTPUT) board"""

    dwg = schemdraw.Drawing(fontsize=12)

    # ==================== TITLE ====================
    dwg += elm.Label().label('PRISME BOTTOM BOARD (OUTPUT BOARD)', fontsize=20)
    dwg += elm.Gap().down(3)

    # ==================== POWER RAILS ====================
    dwg += elm.Label().label('━━━ POWER RAILS ━━━', fontsize=16)
    dwg += elm.Gap().down(1)
    dwg += elm.Label().label('5V from header (C1 47µF, C2 0.1µF) | 3.3V from header (C9 10µF, C10 0.1µF)', loc='left', fontsize=11)
    dwg += elm.Gap().down(4)

    # ==================== CV OUTPUT ====================
    dwg += elm.Label().label('━━━ CV OUTPUT (MCP4728 Channel A) ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Dot().label('CH_A\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(3)
    dwg += elm.Resistor().right().label('R1 100Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Save node
    cv_node_x = dwg.here[0]
    cv_node_y = dwg.here[1]

    # C6 filter to ground - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of capacitor (1.5 units down from cv_node)
    dwg.here = (cv_node_x - 0.6, cv_node_y - 1.5)
    dwg += elm.Label().label('C6\n100nF', fontsize=10)

    # Back to node, continue to output
    dwg.here = (cv_node_x, cv_node_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('CV OUT', loc='right', fontsize=12)

    # CV LED
    dwg.pop()
    dwg += elm.Gap().down(7)
    dwg += elm.Label().label('CV LED:', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D12', loc='left', fontsize=10)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R7 220Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== TRIG OUTPUT ====================
    dwg += elm.Label().label('━━━ TRIG OUTPUT (MCP4728 Channel B) - Dual Mode ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    # V-Trig path
    dwg.push()
    dwg += elm.Label().label('V-Trig (D10=LOW):', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('CH_B\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(3)
    dwg += elm.Resistor().right().label('R2 100Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(6)
    dwg += elm.Dot().label('TRIG OUT', loc='right', fontsize=12)

    # S-Trig path
    dwg.pop()
    dwg += elm.Gap().down(5)
    dwg += elm.Label().label('S-Trig (D10=HIGH):', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg.push()
    dwg += elm.Dot().label('D10', loc='left', fontsize=10)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R5 1kΩ', loc='top', fontsize=11)
    dwg += elm.Line().right(2)
    dwg += elm.BjtNpn().right().anchor('base').label('Q1\n2N3904', loc='bottom', fontsize=10)

    # Save transistor position
    npn_x = dwg.here[0]
    npn_y = dwg.here[1]

    # Collector resistor up to output
    dwg.here = (npn_x + 0.5, npn_y + 0.8)  # Collector position
    dwg += elm.Line().up(1)
    dwg += elm.Resistor().right().label('R6 100Ω', loc='top', fontsize=10)
    dwg += elm.Line().up(2)
    dwg += elm.Dot().label('↑', loc='right', fontsize=10)

    # Emitter to ground
    dwg.here = (npn_x + 0.5, npn_y - 0.8)  # Emitter position
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # RGB LED
    dwg.pop()
    dwg += elm.Gap().down(9)
    dwg += elm.Label().label('TRIG RGB LED:', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)

    dwg.push()
    dwg += elm.Dot().label('A0', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R11 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('RED', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2)
    dwg += elm.Dot().label('A1', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R12 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('GREEN', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(4)
    dwg += elm.Dot().label('A2', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R13 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('BLUE', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== CC OUTPUT ====================
    dwg += elm.Label().label('━━━ CC OUTPUT (MCP4728 Channel C) ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Dot().label('CH_C\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(3)
    dwg += elm.Resistor().right().label('R3 100Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Save node
    cc_node_x = dwg.here[0]
    cc_node_y = dwg.here[1]

    # C7 filter to ground - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of capacitor (1.5 units down from cc_node)
    dwg.here = (cc_node_x - 0.6, cc_node_y - 1.5)
    dwg += elm.Label().label('C7\n100nF', fontsize=10)

    # Back to node, continue to output
    dwg.here = (cc_node_x, cc_node_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('CC OUT', loc='right', fontsize=12)

    # CC LED
    dwg.pop()
    dwg += elm.Gap().down(7)
    dwg += elm.Label().label('CC LED:', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D25', loc='left', fontsize=10)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R8 220Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== MIDI LEDS ====================
    dwg += elm.Label().label('━━━ MIDI INDICATORS ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Dot().label('CAN_TX', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R9 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('MIDI OUT', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2)
    dwg += elm.Dot().label('A5', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R10 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('MIDI IN', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    # ==================== NOTES ====================
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('OPERATION: MCP4728 I2C DAC (0x60), 0-5V outputs | V-Trig: direct | S-Trig: NPN pulls to GND | RGB: GREEN=V-Trig, RED=S-Trig', fontsize=10)

    # Save
    dwg.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/BOTTOM_BOARD_SCHEMATIC.svg')

    print("✅ Bottom board schematic generated")
    return dwg


if __name__ == "__main__":
    generate_bottom_board_schematic()
