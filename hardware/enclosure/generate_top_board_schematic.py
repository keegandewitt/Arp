#!/usr/bin/env python3
"""
PRISME TOP BOARD (INPUT BOARD) - Clean Schematic
Proper label positioning - labels to the SIDE of vertical components
"""

import schemdraw
import schemdraw.elements as elm

def generate_top_board_schematic():
    """Generate schematic for TOP (INPUT) board"""

    dwg = schemdraw.Drawing(fontsize=12)

    # ==================== TITLE ====================
    dwg += elm.Label().label('PRISME TOP BOARD (INPUT BOARD)', fontsize=20)
    dwg += elm.Gap().down(3)

    # ==================== POWER RAILS ====================
    dwg += elm.Label().label('━━━ POWER RAILS ━━━', fontsize=16)
    dwg += elm.Gap().down(1)
    dwg += elm.Label().label('5V from header | 3.3V from header (C11 10µF, C12 0.1µF decoupling)', loc='left', fontsize=11)
    dwg += elm.Gap().down(4)

    # ==================== CV INPUT PROTECTION ====================
    dwg += elm.Label().label('━━━ CV INPUT PROTECTION ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    # Main signal path - horizontal
    dwg.push()
    dwg += elm.Dot().label('CV IN\n±5V', loc='top', fontsize=12)
    dwg += elm.Line().right(3)
    dwg += elm.Resistor().right().label('R14 10kΩ', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Save node position
    node_x = dwg.here[0]
    node_y = dwg.here[1]

    # R15 to ground - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Resistor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of resistor (1.5 units down from node)
    dwg.here = (node_x - 0.6, node_y - 1.5)
    dwg += elm.Label().label('R15\n10kΩ', fontsize=10)

    # Back to node, continue right
    dwg.here = (node_x, node_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('2.62V', loc='top', fontsize=11)

    # Save second node
    node2_x = dwg.here[0]
    node2_y = dwg.here[1]

    # BAT85 clamp - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Diode().down()
    dwg += elm.Line().down(0.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=10)

    # Label at middle of diode (1.5 units down from node2)
    dwg.here = (node2_x - 0.6, node2_y - 1.5)
    dwg += elm.Label().label('D2\nBAT85', fontsize=10)

    # Back to second node, continue to filters
    dwg.here = (node2_x, node2_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot()

    # Save third node
    node3_x = dwg.here[0]
    node3_y = dwg.here[1]

    # C3 filter cap - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of capacitor (1.5 units down from node3)
    dwg.here = (node3_x - 0.6, node3_y - 1.5)
    dwg += elm.Label().label('C3\n100nF', fontsize=10)

    # Back to third node, continue
    dwg.here = (node3_x, node3_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot()

    # Save fourth node
    node4_x = dwg.here[0]
    node4_y = dwg.here[1]

    # C4 second filter cap - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of capacitor (1.5 units down from node4)
    dwg.here = (node4_x - 0.6, node4_y - 1.5)
    dwg += elm.Label().label('C4\n10nF', fontsize=10)

    # Back to fourth node, to ADC
    dwg.here = (node4_x, node4_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('→ A4 ADC', loc='right', fontsize=12)

    # CV LED indicator
    dwg.pop()
    dwg += elm.Gap().down(10)
    dwg += elm.Label().label('CV LED:', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)
    dwg += elm.Dot().label('D5', loc='left', fontsize=11)
    dwg += elm.Line().right(2)
    dwg += elm.Resistor().right().label('R18 220Ω', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('White', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg += elm.Gap().down(4)

    # ==================== TRIG INPUT PROTECTION ====================
    dwg += elm.Label().label('━━━ TRIG INPUT PROTECTION ━━━', fontsize=16)
    dwg += elm.Gap().down(2)

    # Main signal path - horizontal (identical to CV)
    dwg.push()
    dwg += elm.Dot().label('TRIG IN\n±5V', loc='top', fontsize=12)
    dwg += elm.Line().right(3)
    dwg += elm.Resistor().right().label('R16 10kΩ', loc='top', fontsize=11)
    dwg += elm.Line().right(1)
    dwg += elm.Dot()

    # Save node position
    t_node_x = dwg.here[0]
    t_node_y = dwg.here[1]

    # R17 to ground - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Resistor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of resistor (1.5 units down from t_node)
    dwg.here = (t_node_x - 0.6, t_node_y - 1.5)
    dwg += elm.Label().label('R17\n10kΩ', fontsize=10)

    # Back to node, continue right
    dwg.here = (t_node_x, t_node_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('2.62V', loc='top', fontsize=11)

    # Save second node
    t_node2_x = dwg.here[0]
    t_node2_y = dwg.here[1]

    # BAT85 clamp - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Diode().down()
    dwg += elm.Line().down(0.5)
    dwg += elm.Dot().label('3.3V', loc='left', fontsize=10)

    # Label at middle of diode (1.5 units down from t_node2)
    dwg.here = (t_node2_x - 0.6, t_node2_y - 1.5)
    dwg += elm.Label().label('D3\nBAT85', fontsize=10)

    # Back to second node, continue to filter
    dwg.here = (t_node2_x, t_node2_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot()

    # Save third node
    t_node3_x = dwg.here[0]
    t_node3_y = dwg.here[1]

    # C5 filter cap - draw first, then label at middle
    dwg += elm.Line().down(1)
    dwg += elm.Capacitor().down()
    dwg += elm.Line().down(1)
    dwg += elm.Ground()

    # Label at middle of capacitor (1.5 units down from t_node3)
    dwg.here = (t_node3_x - 0.6, t_node3_y - 1.5)
    dwg += elm.Label().label('C5\n100nF', fontsize=10)

    # Back to third node, to ADC
    dwg.here = (t_node3_x, t_node3_y)
    dwg += elm.Line().right(3)
    dwg += elm.Dot().label('→ A3 ADC', loc='right', fontsize=12)

    # TRIG RGB LED
    dwg.pop()
    dwg += elm.Gap().down(10)
    dwg += elm.Label().label('TRIG RGB LED:', loc='left', fontsize=11)
    dwg += elm.Gap().down(0.5)

    dwg.push()
    dwg += elm.Dot().label('D6', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R19 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('RED', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(2)
    dwg += elm.Dot().label('D9', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R20 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('GREEN', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    dwg.pop()
    dwg += elm.Gap().down(4)
    dwg += elm.Dot().label('D11', loc='left', fontsize=10)
    dwg += elm.Line().right(1.5)
    dwg += elm.Resistor().right().label('R21 220Ω', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.LED().right().label('BLUE', loc='top', fontsize=10)
    dwg += elm.Line().right(1)
    dwg += elm.Ground()

    # ==================== NOTES ====================
    dwg += elm.Gap().down(3)
    dwg += elm.Label().label('OPERATION: Voltage dividers scale ±5V→2.62V | BAT85 clamps protect ADC | RC filters remove noise', fontsize=10)

    # Save
    dwg.save('/Users/keegandewitt/Cursor/prisme/hardware/enclosure/TOP_BOARD_SCHEMATIC.svg')

    print("✅ Top board schematic generated")
    return dwg


if __name__ == "__main__":
    generate_top_board_schematic()
