# Schematic Analysis: Broken vs Professional

## BROKEN SCHEMATIC ANALYSIS

**File**: `UNIFIED_SYSTEM_SCHEMATIC.svg`

### Problems Identified:

1. **MASSIVE LABEL OVERLAP**
   - M4 pin labels (A3, A4, D4, D10, etc.) are **inside** the IC box
   - Component values overlap with component symbols
   - Section headers overlap with components
   - Text crowding: "CV IN", "TRIG IN" labels too close to circuits

2. **INCONSISTENT SPACING**
   - CV IN and TRIG IN circuits are different vertical distances apart
   - No consistent horizontal spacing between columns
   - Components randomly spaced

3. **POOR LAYOUT STRUCTURE**
   - Everything crammed into one view
   - No clear signal flow (left → right)
   - M4 in center creates chaos - everything branches from middle

4. **NO GRID ALIGNMENT**
   - Components at random Y positions
   - LEDs not vertically aligned
   - Outputs scattered

5. **TEXT POSITIONING ISSUES**
   - Pin numbers (1, 2, 3...) overlap with pin names (A3, D4...)
   - Labels use mix of positions (some top, some middle, some bottom)
   - Fontsize inconsistent

---

## PROFESSIONAL SCHEMATIC CHARACTERISTICS

**Reference**: Buzzer circuit image provided

### What Makes It Professional:

1. **GENEROUS SPACING**
   - Minimum ~50-60 pixel spacing between components horizontally
   - ~40 pixel spacing vertically between rows
   - Labels have ~15-20 pixel clearance from components
   - No overlaps whatsoever

2. **CLEAR SIGNAL FLOW (Left → Right)**
   - Inputs on left (S1, S2)
   - Processing in middle (resistors, diodes, transistors)
   - Outputs on right (BUZ1, T2)
   - Power rail at top (5V)

3. **GRID ALIGNMENT**
   - All horizontal lines perfectly aligned
   - All ground symbols at same Y level
   - Components in neat rows

4. **CONSISTENT TEXT POSITIONING**
   - Component values ABOVE component
   - Component IDs BELOW or BESIDE component
   - Clear separation (text never overlaps symbols)
   - Uniform font size

5. **CLEAN WIRE ROUTING**
   - Right-angle connections only
   - No diagonal wires except in component symbols
   - Dots at all T-junctions
   - Clear visual hierarchy

6. **FUNCTIONAL GROUPING**
   - Each section has clear boundaries
   - Related components grouped together
   - Visual separation between functional blocks

---

## KEY DIFFERENCES

| Aspect | Broken Schematic | Professional Schematic |
|--------|------------------|----------------------|
| **Spacing** | Random, tight | Consistent, generous (60px H, 40px V) |
| **Flow** | Chaotic (center-out) | Left → Right |
| **Alignment** | Random Y positions | Grid-based |
| **Labels** | Overlapping symbols | Clear separation (~20px offset) |
| **Structure** | Everything in one blob | Functional blocks |
| **Wires** | Complex routing | Right-angle only |

---

## EXTRACTED SPACING RULES

From professional schematic analysis:

### Minimum Spacing (in pixels):
- **Between components (horizontal)**: 50-60px
- **Between rows (vertical)**: 40px
- **Label offset from component**: 15-20px
- **Text line spacing**: 12-15px
- **Section headers above content**: 30px

### In Schemdraw Units (assuming 1 unit ≈ 18px):
- **Between components (horizontal)**: 3.0 units
- **Between rows (vertical)**: 2.2 units
- **Label offset**: 1.0 unit
- **Section spacing**: 1.7 units

---

## ROOT CAUSE OF BROKEN SCHEMATIC

**The code generated the schematic but:**

1. ❌ **No variables stored** - Couldn't reference M4 positions
2. ❌ **No spacing calculations** - Used default element lengths
3. ❌ **No label offset specified** - Used default label positioning
4. ❌ **Improper layout structure** - M4 in center instead of left
5. ❌ **No grid planning** - Random Y positions for outputs

**What should have been done:**

1. ✅ **Store M4 as variable** - Access pin positions later
2. ✅ **Calculate spacing** - H_SPACING=3.0, V_SPACING=2.2
3. ✅ **Explicit label offsets** - `ofst=1.0` on all labels
4. ✅ **Left-to-right layout** - M4 on left, outputs on right
5. ✅ **Grid-based Y positions** - All outputs aligned

---

## RECOMMENDED LAYOUT FOR UNIFIED SCHEMATIC

```
┌────────────────────────────────────────────────────────────┐
│ PRISME HARDWARE SCHEMATIC                                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ [CV IN] ──R1──R2──D1─┐                                    │
│                       │                                    │
│ [TRIG IN]──R4──R5──D2─┤                                   │
│                       │                                    │
│                    ┌──┴──┐        ┌──────────────────┐   │
│                    │     │        │                  │   │
│                    │  M4 ├───A3───┤ MCP4728          │   │
│                    │     │        │  (DAC)           │   │
│                    │     ├───A4───┤                  │   │
│                    │     │        │  VA ───R─── LED ───●│
│                    │     ├───D4───┤  VB ───R─── LED ───●│
│                    │     │        │  VC ───R─── LED ───●│
│                    │     ├───D10──┤                  │   │
│                    │     │        └──────────────────┘   │
│                    └─────┘                               │
│                                                            │
│                    [SDA]──┬── OLED (0x3C)                 │
│                    [SCL]──┘                               │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key features:**
- Inputs on left
- M4 in center-left (not dead center)
- DAC on right with outputs
- Clean sections
- Horizontal signal flow
- Grid alignment

---

## CONFIDENCE LEVEL: 95%

**Why 95% confidence now:**

1. ✅ **Identified exact problems** - Label overlap, no spacing, no grid
2. ✅ **Analyzed professional example** - 60px/40px spacing, left→right flow
3. ✅ **Know the correct approach** - Store variables, calculate grid, explicit offsets
4. ✅ **Have the tools** - `.at()`, `d.move_from()`, `ofst`, `length()`

**Remaining 5% uncertainty:**
- Exact font sizes needed for clean label separation
- Optimal schemdraw unit conversion (pixels → units)
- Whether user wants full system or just M4→outputs

---

## NEXT STEPS

1. Ask user to confirm layout structure:
   - Full system (inputs + M4 + outputs) or just M4→outputs?
   - Horizontal (left→right) or vertical (top→bottom) flow?

2. Generate with these parameters:
   ```python
   H_SPACING = 3.5  # Generous horizontal spacing
   V_SPACING = 2.5  # Generous vertical spacing
   LABEL_OFFSET = 1.0  # Clear label separation
   FONT_SIZE = 11  # Readable text
   ```

3. Use left→right flow with M4 on left, outputs on right

4. Store all components in variables for positioning control

5. Use `d.move_from(m4.pin, dx=X, dy=Y)` for precise row placement
