# Schemdraw Layout Rules - DEFINITIVE GUIDE

**Purpose**: Ground rules for clean schematic generation with schemdraw
**Source**: Official schemdraw documentation + best practices
**Last Updated**: 2025-11-03

---

## 1. ABSOLUTE POSITIONING (THE GOLDEN RULE)

### ✅ ALWAYS USE `.at(x, y)` FOR PRECISE LAYOUTS

**From schemdraw docs:**
```python
.at(position)
  - Positions the element at a specific coordinate.
  - Equivalent to setting attribute `at=X` or `xy=X`.
```

**Rule**: For any schematic with multiple components that need specific spacing, calculate absolute coordinates FIRST, then use `.at((x, y))`.

**Example - CORRECT:**
```python
# Calculate positions first
m4_x = 2
m4_y_base = 5
pin_spacing = 0.5

# Use absolute positioning
d += IC().at((m4_x, m4_y_base)).label('M4')
d += Resistor().at((m4_x + 3, m4_y_base)).label('R1')
d += Resistor().at((m4_x + 3, m4_y_base - pin_spacing)).label('R2')
```

**Example - WRONG (what we were doing):**
```python
# Improvisational chaining = overlap hell
d += IC().label('M4')
d += Resistor().right().label('R1')  # Where does this go? WHO KNOWS!
d += Resistor().down().label('R2')   # Collision incoming!
```

---

## 2. SPACING CONSTANTS

### Standard Schemdraw Units

**From schemdraw pictorial module:**
```python
from schemdraw import pictorial

pictorial.INCH = 2.54  # Convert inches to schemdraw units
pictorial.MILLIMETER = 0.1  # Convert mm to schemdraw units
pictorial.PINSPACING = 0.254  # Standard 0.1 inch spacing
```

### Recommended Minimum Spacing

Based on schemdraw element sizes and label positioning:

| Element Type | Minimum Horizontal Spacing | Minimum Vertical Spacing |
|--------------|---------------------------|-------------------------|
| Resistor/Capacitor | 2.0 units | 1.0 units |
| IC/Component | 3.0 units | 1.5 units |
| Wire/Line | 0.5 units | 0.5 units |
| Labels (no overlap) | 1.0 unit offset | 0.5 unit offset |

**Rule**: Use `spacing = 2.0` as default for components, increase to 3.0 for ICs.

---

## 3. LABEL POSITIONING

### Label Offset Parameters

**From schemdraw docs:**
```python
.label(text, ofst=value)
  - ofst: single value = vertical offset
  - ofst: (x, y) tuple = horizontal and vertical offset
```

**Standard Label Positions:**
```python
.label('Text', loc='top')      # Above component
.label('Text', loc='bottom')   # Below component
.label('Text', loc='left')     # Left of component
.label('Text', loc='right')    # Right of component
```

### Label Offset Rules

**Minimum offset to avoid overlap:**
- `ofst=0.3` - Minimum offset for single-line labels
- `ofst=0.5` - Standard offset for readability
- `ofst=(x, y)` - Use tuple for precise positioning

**Example - CORRECT:**
```python
d += Resistor().at((5, 10)).label('R1\n10kΩ', loc='top', ofst=0.5, fontsize=9)
# Label is 0.5 units above resistor, won't overlap with component above
```

**Example - WRONG:**
```python
d += Resistor().label('R1\n10kΩ')  # Default ofst, may overlap!
```

---

## 4. ALIGNMENT AND ANCHORS

### Using Anchors for Precise Connections

**From schemdraw docs:**
```python
.anchor(anchor_point)
  - Sets the anchor point for positioning.
  - Common anchors: 'start', 'end', 'center'
```

**Access absolute anchor positions:**
```python
element.absanchors['anchor_name']  # Returns (x, y) tuple
```

**Rule**: Use anchors to get exact positions for connecting elements.

**Example:**
```python
# Position IC
m4 = IC().at((2, 5)).label('M4')

# Get exact pin position
pin_a3_pos = m4.absanchors['p3']  # If IC has named pins

# Position next element at exact pin location
d += Line().at(pin_a3_pos).right().length(1.0)
```

---

## 5. GRID-BASED LAYOUT STRATEGY

### The Coordinate Planning Method

**Step 1: Define Grid**
```python
# Define coordinate system
origin_x = 0
origin_y = 0
component_spacing_x = 3.0
component_spacing_y = 1.5
```

**Step 2: Calculate All Positions**
```python
# Calculate positions BEFORE drawing
m4_pos = (origin_x, origin_y)
r1_pos = (origin_x + component_spacing_x, origin_y)
r2_pos = (origin_x + component_spacing_x, origin_y - component_spacing_y)
led1_pos = (origin_x + component_spacing_x * 2, origin_y)
```

**Step 3: Draw with Absolute Positioning**
```python
d += IC().at(m4_pos).label('M4')
d += Resistor().at(r1_pos).label('R1')
d += Resistor().at(r2_pos).label('R2')
d += LED().at(led1_pos).label('LED1')
```

**Rule**: NEVER mix relative positioning (`.right()`, `.down()`) with absolute positioning in the same schematic.

---

## 6. WIRE ROUTING

### Use Intermediate Points

**From schemdraw docs:**
```python
d += Line().at(start_pos).to(end_pos)  # Direct line
d += Wire('c').at(start_pos).to(end_pos)  # Cornell wire (right angles)
```

**For Complex Routing:**
```python
# Define waypoints
start = (2, 5)
waypoint1 = (4, 5)
waypoint2 = (4, 3)
end = (6, 3)

# Draw segments
d += Line().at(start).to(waypoint1)
d += Line().at(waypoint1).to(waypoint2)
d += Line().at(waypoint2).to(end)
```

**Rule**: For clean schematics, route wires with explicit waypoints, not chained `.right().down()` calls.

---

## 7. LABEL ALIGNMENT

### Horizontal and Vertical Alignment

**From schemdraw docs:**
```python
.label(text, halign='left')    # 'left', 'center', 'right'
.label(text, valign='center')  # 'top', 'center', 'bottom', 'base'
```

**Rule**: Always specify alignment for multi-component schematics to ensure consistency.

**Example:**
```python
d += Resistor().at((5, 10)).label('R1\n10kΩ',
                                   loc='top',
                                   ofst=0.5,
                                   halign='center',
                                   fontsize=9)
```

---

## 8. MULTI-COMPONENT LAYOUT ALGORITHM

### The Correct Approach (3-Step Process)

**Step 1: Define Layout Parameters**
```python
# Spacing constants
H_SPACING = 3.0      # Horizontal spacing between components
V_SPACING = 1.5      # Vertical spacing between rows
LABEL_OFFSET = 0.5   # Label offset from component
FONT_SIZE = 9        # Standard font size

# Grid origin
ORIGIN_X = 1.0
ORIGIN_Y = 10.0
```

**Step 2: Calculate All Component Positions**
```python
# Create position dictionary
positions = {
    'm4': (ORIGIN_X, ORIGIN_Y),
    'r1': (ORIGIN_X + H_SPACING, ORIGIN_Y),
    'r2': (ORIGIN_X + H_SPACING, ORIGIN_Y - V_SPACING),
    'led1': (ORIGIN_X + H_SPACING * 2, ORIGIN_Y),
    # ... calculate ALL positions before drawing
}
```

**Step 3: Draw Using Absolute Positions**
```python
d = schemdraw.Drawing()

# M4 IC
d += IC().at(positions['m4']).label('M4', fontsize=FONT_SIZE)

# Resistors
d += Resistor().at(positions['r1']).label('R1\n10kΩ',
                                           loc='top',
                                           ofst=LABEL_OFFSET,
                                           fontsize=FONT_SIZE)

d += Resistor().at(positions['r2']).label('R2\n10kΩ',
                                           loc='top',
                                           ofst=LABEL_OFFSET,
                                           fontsize=FONT_SIZE)

# LED
d += LED().at(positions['led1']).label('LED1',
                                        loc='right',
                                        ofst=LABEL_OFFSET,
                                        fontsize=FONT_SIZE)

d.save('clean_schematic.svg')
```

---

## 9. COMMON PITFALLS TO AVOID

### ❌ DON'T: Improvisational Chaining
```python
# This creates unpredictable spacing and overlaps
d += IC()
d += Resistor().right()  # How far right? Unknown!
d += LED().down()        # Collision likely!
```

### ❌ DON'T: Mix Absolute and Relative
```python
# Mixing .at() and .right() is chaos
d += IC().at((2, 5))
d += Resistor().right()  # Where is this? Based on IC? Last position? WHO KNOWS!
```

### ❌ DON'T: Default Label Positions for Dense Layouts
```python
# Labels will overlap in dense layouts
d += Resistor().label('R1')
d += Resistor().at((2.5, 5)).label('R2')  # R2 label may overlap R1!
```

### ✅ DO: Plan, Calculate, Position
```python
# Define positions
r1_pos = (2, 5)
r2_pos = (5, 5)  # 3 units apart (safe spacing)

# Draw with absolute positioning and explicit label offsets
d += Resistor().at(r1_pos).label('R1\n10kΩ', loc='top', ofst=0.5, fontsize=9)
d += Resistor().at(r2_pos).label('R2\n10kΩ', loc='top', ofst=0.5, fontsize=9)
```

---

## 10. DEBUGGING OVERLAPS

### Troubleshooting Checklist

When components or labels overlap:

1. **Check spacing values**:
   - Are H_SPACING and V_SPACING large enough?
   - Minimum 2.0 for components, 3.0 for ICs

2. **Check label offsets**:
   - Are labels using `ofst` parameter?
   - Minimum 0.3, recommended 0.5

3. **Check positioning method**:
   - Are you using `.at((x, y))` for everything?
   - NO relative positioning (`.right()`, `.down()`) in dense layouts

4. **Verify calculations**:
   - Print position dictionary before drawing
   - Check for duplicate coordinates

5. **Increase spacing**:
   - Try doubling H_SPACING and V_SPACING temporarily
   - If overlap disappears, gradually reduce until optimal

---

## 11. TEMPLATE FOR CLEAN SCHEMATICS

```python
import schemdraw
from schemdraw import elements as elm

# 1. DEFINE LAYOUT PARAMETERS
H_SPACING = 3.0
V_SPACING = 1.5
LABEL_OFFSET = 0.5
FONT_SIZE = 9
ORIGIN_X = 1.0
ORIGIN_Y = 10.0

# 2. CALCULATE POSITIONS
positions = {
    'component1': (ORIGIN_X, ORIGIN_Y),
    'component2': (ORIGIN_X + H_SPACING, ORIGIN_Y),
    'component3': (ORIGIN_X + H_SPACING * 2, ORIGIN_Y),
    # ... calculate all positions
}

# 3. CREATE DRAWING
d = schemdraw.Drawing()

# 4. ADD ELEMENTS WITH ABSOLUTE POSITIONING
d += elm.Resistor().at(positions['component1']).label(
    'R1\n10kΩ',
    loc='top',
    ofst=LABEL_OFFSET,
    halign='center',
    fontsize=FONT_SIZE
)

d += elm.Capacitor().at(positions['component2']).label(
    'C1\n100nF',
    loc='top',
    ofst=LABEL_OFFSET,
    halign='center',
    fontsize=FONT_SIZE
)

d += elm.LED().at(positions['component3']).label(
    'LED1',
    loc='right',
    ofst=LABEL_OFFSET,
    fontsize=FONT_SIZE
)

# 5. SAVE
d.save('schematic.svg')
```

---

## SUMMARY: THE 3 COMMANDMENTS

1. **CALCULATE FIRST, DRAW SECOND**
   - Define all X, Y coordinates before calling `schemdraw.Drawing()`
   - Store in a positions dictionary
   - Never guess positions while drawing

2. **ABSOLUTE POSITIONING ONLY**
   - Use `.at((x, y))` for every component
   - NO `.right()`, `.down()`, `.up()`, `.left()` in dense layouts
   - Exception: Simple single-path schematics with no overlaps

3. **EXPLICIT LABEL POSITIONING**
   - Always specify `loc`, `ofst`, `halign`, `fontsize`
   - Never rely on defaults for multi-component schematics
   - Minimum ofst=0.3, recommended ofst=0.5

---

**Follow these rules and overlaps will NEVER happen.**
