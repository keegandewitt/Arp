"""
MIDI CC Names - Universal Standard Names
Abbreviated for OLED display (21 char max width)

Used by Custom CC menu to display user-friendly CC names.
"""

# Full MIDI CC name mapping (0-127)
# Format: CC Number → (Short Name for OLED, Full Name)
MIDI_CC_NAMES = {
    # 0-31: High-resolution continuous controllers (MSB)
    0: ("Bank Select MSB", "Bank Select (MSB)"),
    1: ("Mod Wheel", "Modulation Wheel"),
    2: ("Breath Ctrl", "Breath Controller"),
    3: ("CC 3", "Undefined CC 3"),
    4: ("Foot Ctrl", "Foot Controller"),
    5: ("Portamento Time", "Portamento Time"),
    6: ("Data Entry MSB", "Data Entry (MSB)"),
    7: ("Volume", "Channel Volume"),
    8: ("Balance", "Balance"),
    9: ("CC 9", "Undefined CC 9"),
    10: ("Pan", "Pan"),
    11: ("Expression", "Expression Controller"),
    12: ("Effect 1", "Effect Control 1"),
    13: ("Effect 2", "Effect Control 2"),
    14: ("CC 14", "Undefined CC 14"),
    15: ("CC 15", "Undefined CC 15"),
    16: ("Gen Purpose 1", "General Purpose 1"),
    17: ("Gen Purpose 2", "General Purpose 2"),
    18: ("Gen Purpose 3", "General Purpose 3"),
    19: ("Gen Purpose 4", "General Purpose 4"),

    # 20-31: Undefined/manufacturer-specific
    20: ("CC 20", "Undefined CC 20"),
    21: ("CC 21", "Undefined CC 21"),
    22: ("CC 22", "Undefined CC 22"),
    23: ("CC 23", "Undefined CC 23"),
    24: ("CC 24", "Undefined CC 24"),
    25: ("CC 25", "Undefined CC 25"),
    26: ("CC 26", "Undefined CC 26"),
    27: ("CC 27", "Undefined CC 27"),
    28: ("CC 28", "Undefined CC 28"),
    29: ("CC 29", "Undefined CC 29"),
    30: ("CC 30", "Undefined CC 30"),
    31: ("CC 31", "Undefined CC 31"),

    # 32-63: LSB for CC 0-31 (low-resolution counterparts)
    32: ("Bank Select LSB", "Bank Select (LSB)"),
    33: ("Mod Wheel LSB", "Modulation Wheel (LSB)"),
    34: ("Breath Ctrl LSB", "Breath Controller (LSB)"),
    35: ("CC 35 LSB", "Undefined CC 35 (LSB)"),
    36: ("Foot Ctrl LSB", "Foot Controller (LSB)"),
    37: ("Portamento LSB", "Portamento Time (LSB)"),
    38: ("Data Entry LSB", "Data Entry (LSB)"),
    39: ("Volume LSB", "Channel Volume (LSB)"),
    40: ("Balance LSB", "Balance (LSB)"),
    41: ("CC 41 LSB", "Undefined CC 41 (LSB)"),
    42: ("Pan LSB", "Pan (LSB)"),
    43: ("Expression LSB", "Expression (LSB)"),
    44: ("Effect 1 LSB", "Effect Control 1 (LSB)"),
    45: ("Effect 2 LSB", "Effect Control 2 (LSB)"),
    46: ("CC 46 LSB", "Undefined CC 46 (LSB)"),
    47: ("CC 47 LSB", "Undefined CC 47 (LSB)"),
    48: ("Gen Purpose 1 LSB", "General Purpose 1 (LSB)"),
    49: ("Gen Purpose 2 LSB", "General Purpose 2 (LSB)"),
    50: ("Gen Purpose 3 LSB", "General Purpose 3 (LSB)"),
    51: ("Gen Purpose 4 LSB", "General Purpose 4 (LSB)"),
    52: ("CC 52 LSB", "Undefined CC 52 (LSB)"),
    53: ("CC 53 LSB", "Undefined CC 53 (LSB)"),
    54: ("CC 54 LSB", "Undefined CC 54 (LSB)"),
    55: ("CC 55 LSB", "Undefined CC 55 (LSB)"),
    56: ("CC 56 LSB", "Undefined CC 56 (LSB)"),
    57: ("CC 57 LSB", "Undefined CC 57 (LSB)"),
    58: ("CC 58 LSB", "Undefined CC 58 (LSB)"),
    59: ("CC 59 LSB", "Undefined CC 59 (LSB)"),
    60: ("CC 60 LSB", "Undefined CC 60 (LSB)"),
    61: ("CC 61 LSB", "Undefined CC 61 (LSB)"),
    62: ("CC 62 LSB", "Undefined CC 62 (LSB)"),
    63: ("CC 63 LSB", "Undefined CC 63 (LSB)"),

    # 64-69: Switches (0-63 = off, 64-127 = on)
    64: ("Sustain Pedal", "Sustain Pedal (Damper)"),
    65: ("Portamento", "Portamento On/Off"),
    66: ("Sostenuto", "Sostenuto Pedal"),
    67: ("Soft Pedal", "Soft Pedal"),
    68: ("Legato", "Legato Footswitch"),
    69: ("Hold 2", "Hold 2"),

    # 70-79: Sound controllers
    70: ("Sound Variation", "Sound Controller 1 (Sound Variation)"),
    71: ("Filter Resonance", "Sound Controller 2 (Resonance/Timbre)"),
    72: ("Release Time", "Sound Controller 3 (Release Time)"),
    73: ("Attack Time", "Sound Controller 4 (Attack Time)"),
    74: ("Filter Cutoff", "Sound Controller 5 (Brightness/Cutoff)"),
    75: ("Decay Time", "Sound Controller 6 (Decay Time)"),
    76: ("Vibrato Rate", "Sound Controller 7 (Vibrato Rate)"),
    77: ("Vibrato Depth", "Sound Controller 8 (Vibrato Depth)"),
    78: ("Vibrato Delay", "Sound Controller 9 (Vibrato Delay)"),
    79: ("Sound Ctrl 10", "Sound Controller 10"),

    # 80-83: General purpose switches
    80: ("Gen Purpose 5", "General Purpose Controller 5"),
    81: ("Gen Purpose 6", "General Purpose Controller 6"),
    82: ("Gen Purpose 7", "General Purpose Controller 7"),
    83: ("Gen Purpose 8", "General Purpose Controller 8"),

    # 84-90: Undefined
    84: ("Portamento Ctrl", "Portamento Control"),
    85: ("CC 85", "Undefined CC 85"),
    86: ("CC 86", "Undefined CC 86"),
    87: ("CC 87", "Undefined CC 87"),
    88: ("CC 88", "Undefined CC 88"),
    89: ("CC 89", "Undefined CC 89"),
    90: ("CC 90", "Undefined CC 90"),

    # 91-95: Effects depth
    91: ("Reverb Send", "Effects 1 Depth (Reverb Send)"),
    92: ("Tremolo Depth", "Effects 2 Depth (Tremolo)"),
    93: ("Chorus Send", "Effects 3 Depth (Chorus Send)"),
    94: ("Detune Depth", "Effects 4 Depth (Detune/Celeste)"),
    95: ("Phaser Depth", "Effects 5 Depth (Phaser)"),

    # 96-101: Data controllers
    96: ("Data Increment", "Data Increment (+1)"),
    97: ("Data Decrement", "Data Decrement (-1)"),
    98: ("NRPN LSB", "Non-Registered Parameter (LSB)"),
    99: ("NRPN MSB", "Non-Registered Parameter (MSB)"),
    100: ("RPN LSB", "Registered Parameter (LSB)"),
    101: ("RPN MSB", "Registered Parameter (MSB)"),

    # 102-119: Undefined
    102: ("CC 102", "Undefined CC 102"),
    103: ("CC 103", "Undefined CC 103"),
    104: ("CC 104", "Undefined CC 104"),
    105: ("CC 105", "Undefined CC 105"),
    106: ("CC 106", "Undefined CC 106"),
    107: ("CC 107", "Undefined CC 107"),
    108: ("CC 108", "Undefined CC 108"),
    109: ("CC 109", "Undefined CC 109"),
    110: ("CC 110", "Undefined CC 110"),
    111: ("CC 111", "Undefined CC 111"),
    112: ("CC 112", "Undefined CC 112"),
    113: ("CC 113", "Undefined CC 113"),
    114: ("CC 114", "Undefined CC 114"),
    115: ("CC 115", "Undefined CC 115"),
    116: ("CC 116", "Undefined CC 116"),
    117: ("CC 117", "Undefined CC 117"),
    118: ("CC 118", "Undefined CC 118"),
    119: ("CC 119", "Undefined CC 119"),

    # 120-127: Channel mode messages
    120: ("All Sound Off", "All Sound Off"),
    121: ("Reset All Ctrl", "Reset All Controllers"),
    122: ("Local Control", "Local Control On/Off"),
    123: ("All Notes Off", "All Notes Off"),
    124: ("Omni Mode Off", "Omni Mode Off"),
    125: ("Omni Mode On", "Omni Mode On"),
    126: ("Mono Mode", "Mono Mode On (Poly Off)"),
    127: ("Poly Mode", "Poly Mode On (Mono Off)"),
}

# Commonly used CCs for quick reference (most important for synth control)
COMMON_CCS = {
    1: "Mod Wheel",
    7: "Volume",
    10: "Pan",
    11: "Expression",
    64: "Sustain Pedal",
    71: "Filter Resonance",
    74: "Filter Cutoff",
}

# Get short name for OLED display
def get_cc_short_name(cc_number):
    """
    Get abbreviated CC name for OLED display.
    Returns: "CC X: Short Name" format
    """
    if cc_number in MIDI_CC_NAMES:
        short_name = MIDI_CC_NAMES[cc_number][0]
        return f"CC {cc_number}: {short_name}"
    return f"CC {cc_number}: Unknown"

# Get full name for documentation/debugging
def get_cc_full_name(cc_number):
    """
    Get full CC name.
    Returns: Full descriptive name
    """
    if cc_number in MIDI_CC_NAMES:
        return MIDI_CC_NAMES[cc_number][1]
    return f"Undefined CC {cc_number}"

# Check if CC is commonly used
def is_common_cc(cc_number):
    """Check if this CC is in the commonly used list"""
    return cc_number in COMMON_CCS
