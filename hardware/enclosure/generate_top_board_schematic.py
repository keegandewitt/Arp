#!/usr/bin/env python3
"""
PRISME TOP BOARD (INPUT BOARD) - Complete Production Schematic
Includes: Feather M4, OLED FeatherWing, CV/TRIG input protection circuits
"""

import schemdraw
import schemdraw.elements as elm

def generate_top_board_schematic():
    """Generate complete schematic for TOP (INPUT) board"""

    dwg = schemdraw.Drawing(fontsize=12)

    # ==================== TITLE ====================
    dwg += elm.Label().label('PRISME TOP BOARD (INPUT BOARD) - Complete Schematic', fontsize=20)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Board: 90mm × 55mm custom-cut ElectroCookie protoboard | Position: Middle layer', fontsize=10)
    dwg += elm.Gap().down(4)

    # ==================== FEATHER M4 + OLED SECTION ====================
    dwg += elm.Label().label('------ MAIN CONTROLLER STACK ------', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    # OLED FeatherWing (top of stack)
    dwg += elm.Label().label('+─────────────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  OLED FeatherWing 128×64       |', fontsize=11)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  (SH1107 driver, I2C 0x3C)     |', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  Buttons: A(D5), B(D6), C(D9)  |', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('+─────────────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('         UPDOWN Stacking Headers', fontsize=9)
    dwg += elm.Gap().down(0.5)

    # Feather M4 (base of stack)
    dwg += elm.Label().label('+─────────────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  Feather M4 CAN Express        |', fontsize=11)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  ATSAMD51, 120MHz, 192KB RAM   |', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('|  CircuitPython 10.0.3          |', fontsize=10)
    dwg += elm.Gap().down(0.8)
    dwg += elm.Label().label('+─────────────────────────────────+', fontsize=10)
    dwg += elm.Gap().down(1)

    # Key connections from M4
    dwg += elm.Label().label('Key Connections:', fontsize=11)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('I2C: D21(SDA), D22(SCL) -> OLED + MCP4728', fontsize=9)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('MIDI: D0(RX), D1(TX) -> Bottom board', fontsize=9)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('ADC: A3(TRIG), A4(CV) <- Input circuits', fontsize=9)
    dwg += elm.Gap().down(0.6)
    dwg += elm.Label().label('GPIO: D4-D25, A0-A5 -> LEDs, S-Trig', fontsize=9)

    dwg.pop()
    dwg += elm.Gap().down(20)

    # ==================== POWER SECTION ====================
    dwg += elm.Label().label('------ POWER DISTRIBUTION ------', fontsize=16)
    dwg += elm.Gap().down(2)

    dwg.push()
    dwg += elm.Label().label('5V Rail (from headers):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('5V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C11 10uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2.5)
    dwg += elm.Dot().label('5V', loc='left', fontsize=11)
    dwg += elm.Line().right(1.5)
    dwg += elm.Capacitor().right().label('C12 0.1uF', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== CV INPUT PROTECTION ====================
    dwg += elm.Label().label('------ CV INPUT PROTECTION (Rear Jack -> A4 ADC) ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Purpose: Scale 0-5V input -> 0-2.62V safe for 3.3V ADC | BAT85 clamp protects from overvoltage', fontsize=10)
    dwg += elm.Gap().down(2)

    # Main signal path
    dwg.push()
    dwg += elm.Dot().label('CV IN\nJack\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R14 10kΩ', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Node 1: Voltage divider
    node1_x = dwg.here[0]
    node1_y = dwg.here[1]

    # R15 to ground
    dwg += elm.Line().down(1)
    dwg += elm.Resistor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (node1_x - 0.6, node1_y - 1.5)
    dwg += elm.Label().label('R15\n10kΩ', fontsize=10)

    # Continue from node 1
    dwg.here = (node1_x, node1_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('2.62V\nmax', loc='top', fontsize=10)

    # Node 2: Clamp diode
    node2_x = dwg.here[0]
    node2_y = dwg.here[1]

    # BAT85 to 3.3V
    dwg += elm.Line().down(1)
    dwg += elm.Diode().down()
    dwg += elm.Line().down(0.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=10)
    dwg.here = (node2_x - 0.6, node2_y - 1.5)
    dwg += elm.Label().label('D2\nBAT85', fontsize=10)

    # Continue to filters
    dwg.here = (node2_x, node2_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot()

    # Node 3: First filter cap
    node3_x = dwg.here[0]
    node3_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (node3_x - 0.6, node3_y - 1.5)
    dwg += elm.Label().label('C3\n100nF', fontsize=10)

    # Continue to second filter
    dwg.here = (node3_x, node3_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot()

    # Node 4: Second filter cap
    node4_x = dwg.here[0]
    node4_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (node4_x - 0.6, node4_y - 1.5)
    dwg += elm.Label().label('C4\n10nF', fontsize=10)

    # To ADC
    dwg.here = (node4_x, node4_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('-> A4\nADC', loc='right', fontsize=12)

    # CV LED indicator
    dwg.pop()
    dwg += elm.Gap().down(11)
    dwg += elm.Label().label('CV Activity LED (rear panel, 7mm right of jack):', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D5', loc='left', fontsize=11)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R18 150Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White 3mm', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== TRIG INPUT PROTECTION ====================
    dwg += elm.Label().label('------ TRIG INPUT PROTECTION (Rear Jack -> A3 ADC) ------', fontsize=16)
    dwg += elm.Gap().down(2)
    dwg += elm.Label().label('Purpose: Identical to CV input | Scale 0-5V input -> 0-2.62V safe for 3.3V ADC', fontsize=10)
    dwg += elm.Gap().down(2)

    # Main signal path
    dwg.push()
    dwg += elm.Dot().label('TRIG IN\nJack\n0-5V', loc='top', fontsize=12)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R16 10kΩ', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Node 1
    t_node1_x = dwg.here[0]
    t_node1_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Resistor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (t_node1_x - 0.6, t_node1_y - 1.5)
    dwg += elm.Label().label('R17\n10kΩ', fontsize=10)

    dwg.here = (t_node1_x, t_node1_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('2.62V\nmax', loc='top', fontsize=10)

    # Node 2
    t_node2_x = dwg.here[0]
    t_node2_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Diode().down()
    dwg += elm.Line().down(0.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=10)
    dwg.here = (t_node2_x - 0.6, t_node2_y - 1.5)
    dwg += elm.Label().label('D3\nBAT85', fontsize=10)

    dwg.here = (t_node2_x, t_node2_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot()

    # Node 3
    t_node3_x = dwg.here[0]
    t_node3_y = dwg.here[1]

    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()
    dwg.here = (t_node3_x - 0.6, t_node3_y - 1.5)
    dwg += elm.Label().label('C5\n100nF', fontsize=10)

    dwg.here = (t_node3_x, t_node3_y)
    dwg += elm.Line().right(2)
    dwg += elm.Dot().label('-> A3\nADC', loc='right', fontsize=12)

    # TRIG RGB LED
    dwg.pop()
    dwg += elm.Gap().down(11)
    dwg += elm.Label().label('TRIG Mode/Activity RGB LED (rear panel, 7mm right of jack):', fontsize=11)
    dwg += elm.Gap().down(0.5)

    dwg.push()
    dwg += elm.Dot().label('D6 (RED)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R19 150Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('RED', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2)
    dwg += elm.Dot().label('D9 (GRN)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R20 150Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('GREEN', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(4)
    dwg += elm.Dot().label('D11 (BLU)', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R21 150Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('BLUE', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    # ==================== NOTES ====================
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('NOTES:', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• Voltage dividers (R14-R15, R16-R17) scale 5V -> 2.62V for safe ADC operation', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• BAT85 Schottky diodes clamp overvoltage to 3.3V (protection from >5V inputs)', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• Dual-stage RC filtering (100nF + 10nF) removes high-frequency noise and RF interference', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• RGB LED: GREEN = V-Trig mode | RED = S-Trig mode | Activity = brightness', fontsize=9)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Label().label('• All decoupling caps close to power pins: C11 (bulk), C12 (bypass)', fontsize=9)

    # Save
    dwg.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_BOARD_SCHEMATIC.svg')

    print("✅ Top board schematic generated (complete with Feather M4 and OLED)")
    return dwg


if __name__ == "__main__":
    generate_top_board_schematic()
