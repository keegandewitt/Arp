# Schemdraw Assumptions - VERIFIED AGAINST OFFICIAL DOCS

**Source**: https://schemdraw.readthedocs.io/en/latest/usage/placement.html
**Date**: 2025-11-03

---

## VERIFICATION RESULTS

### ✅ ASSUMPTION 1: Absolute positioning with `.at()` prevents overlaps

**Official Documentation Says:**
> "Alternatively, one element can be placed starting on the anchor of another element using the at method."

**Example from docs:**
```python
with schemdraw.Drawing():
    opamp = elm.Opamp()
    elm.Resistor().right().at(opamp.out)
```

**VERIFIED**: ✅ YES - `.at((x, y))` or `.at(anchor)` places elements at exact positions

**IMPORTANT CLARIFICATION FROM DOCS:**
> "The Drawing maintains a current position and direction, such that the default placement of the next element will start at the end of the previous element, going in the same direction."

**This means:**
- WITHOUT `.at()`: Elements chain automatically (current position → next element)
- WITH `.at()`: Elements placed at EXACT position, breaking the chain
- **Both methods are valid**, choice depends on use case

---

### ⚠️ ASSUMPTION 2: Chaining `.right()` and `.down()` causes overlaps

**Official Documentation Shows:**
```python
with schemdraw.Drawing():
    elm.Capacitor()
    elm.Resistor().up()  # Changes direction
    elm.Diode()          # Continues in new direction
```

**FINDING**: ❌ **CHAINING DOES NOT INHERENTLY CAUSE OVERLAPS**

**What the docs show:**
- Chaining `.right()`, `.down()`, etc. is **THE STANDARD METHOD** for simple sequential circuits
- Elements auto-connect end-to-end
- This is the **recommended approach** for linear schematics

**The ACTUAL problem with previous attempts:**
- Not calculating **element lengths** properly
- Not accounting for **label space requirements**
- Not using **spacing parameters** for dense layouts

---

### ✅ ASSUMPTION 3: Label offset with `ofst` prevents overlap

**Official Documentation Says:**
```python
elm.Resistor().label('offset', ofst=1)
elm.Resistor().label('offset (x, y)', ofst=(-.6, .2))
```

**VERIFIED**: ✅ YES - `ofst` parameter controls label position relative to element

**Label positioning options:**
- `ofst=float` - Vertical offset only
- `ofst=(x, y)` - Both horizontal and vertical offset
- `loc='top'|'bottom'|'left'|'right'` - Base position
- `halign='left'|'center'|'right'` - Horizontal alignment
- `valign='top'|'center'|'bottom'` - Vertical alignment

---

## KEY FINDING: TWO VALID APPROACHES

### Approach A: Sequential Chaining (Recommended for simple circuits)

**When to use:**
- Linear signal flow (left→right, top→bottom)
- Simple circuits with few branches
- When you want automatic connections

**Example from docs:**
```python
with schemdraw.Drawing():
    elm.Resistor().label('100KΩ')
    elm.Capacitor().down().label('0.1μF', loc='bottom')
    elm.Line().left()
    elm.Ground()
    elm.SourceV().up().label('10V')
```

**Key insight**: This works BECAUSE elements know their own size and auto-space

---

### Approach B: Absolute Positioning (Recommended for complex layouts)

**When to use:**
- Complex layouts with multiple parallel branches
- When you need precise control over spacing
- When elements need to align in a grid

**How to use:**
1. Store elements in variables
2. Use `.at(element.anchor)` to position next element
3. Access absolute positions with `element.absanchors['name']`

**Example from docs:**
```python
with schemdraw.Drawing() as d:
    elm.Line().length(2)
    bjt = elm.BjtNpn()

# Access absolute position
print('absanchor: ', bjt.absanchors['base'])  # Point(2.0, 0.0)

# Use for positioning next element
elm.Resistor().at(bjt.collector)
```

---

## THE REAL PROBLEM WITH PREVIOUS ATTEMPTS

Based on documentation review, the issues were likely:

### 1. **Not Using Element Variables**
```python
# ❌ WRONG - Can't reference positions later
d += IC().label('M4')
d += Resistor().right().label('R1')  # Where is M4? Can't access it!

# ✅ CORRECT - Store for later reference
m4 = d += IC().label('M4')
r1 = d += Resistor().at(m4.p3).right().label('R1')
```

### 2. **Not Accounting for Label Space**
```python
# ❌ WRONG - Default label position may overlap
d += Resistor().label('R1\n10kΩ')
d += Resistor().right().label('R2\n10kΩ')  # Labels may collide!

# ✅ CORRECT - Explicit offset
d += Resistor().label('R1\n10kΩ', loc='top', ofst=0.5)
d += Resistor().right().label('R2\n10kΩ', loc='top', ofst=0.5)
```

### 3. **Not Using Length Parameter for Spacing**
```python
# ❌ WRONG - Default lengths may be too tight
d += Resistor()
d += Capacitor().right()  # Only default spacing

# ✅ CORRECT - Explicit spacing with length
d += Resistor()
d += Line().right().length(2)  # Add spacing
d += Capacitor()
```

### 4. **Complex Branching Without Anchors**
```python
# ❌ WRONG - Branching without reference points
d += IC()
d += Resistor().right()  # From where on IC?
d += LED().down()        # From where on resistor?

# ✅ CORRECT - Use anchors and variables
m4 = d += IC().label('M4')
r1 = d += Resistor().at(m4.p3).right().length(3)
led = d += LED().at(r1.end).down()
```

---

## CORRECTED RULES FOR CLEAN SCHEMATICS

### Rule 1: **Store Elements in Variables**
```python
element = d += elm.Component()
# NOT just: d += elm.Component()
```

### Rule 2: **Use Anchors for Branching**
```python
next_element = d += elm.NextComponent().at(element.anchor_name)
```

### Rule 3: **Add Explicit Spacing for Dense Layouts**
```python
d += elm.Line().length(2)  # Spacing line
# OR
d += elm.Component().at((x, y))  # Jump to position
```

### Rule 4: **Always Specify Label Parameters**
```python
.label('Text', loc='top', ofst=0.5, halign='center', fontsize=9)
```

### Rule 5: **Use `d.move()` or `d.push()/pop()` for Complex Layouts**
```python
with schemdraw.Drawing() as d:
    elm.Resistor()
    d.push()  # Save position
    elm.Capacitor().down()
    d.pop()   # Return to saved position
    elm.Diode()
```

---

## RECOMMENDED APPROACH FOR UNIFIED SCHEMATIC

### Option 1: Hybrid Approach (RECOMMENDED)

**Use chaining for main flow + anchors for branches:**

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing() as d:
    # Main component with stored reference
    m4 = elm.IcDIP(pins=8).label('M4')

    # Branch to outputs using anchors
    d.move_from(m4.p1, dx=3, dy=0)  # Move to output position
    r1 = elm.Resistor().right().length(2).label('R1\n10kΩ', loc='top', ofst=0.5)
    led1 = elm.LED().right().label('LED1', loc='right', ofst=0.3)

    # Add spacing and next row
    d.move_from(m4.p2, dx=3, dy=0)
    r2 = elm.Resistor().right().length(2).label('R2\n10kΩ', loc='top', ofst=0.5)
    led2 = elm.LED().right().label('LED2', loc='right', ofst=0.3)
```

**Why this works:**
- Stores M4 for anchor reference
- Uses `d.move_from()` for precise positioning
- Uses chaining for linear connections
- Explicit length for spacing
- Explicit label parameters

---

## FINAL ANSWER: WHAT TO DO NEXT

### For Your Unified Schematic:

1. **Choose the layout structure** (left-to-right? top-to-bottom?)
2. **Store M4 IC in a variable**
3. **Use `d.move_from(m4.pin, dx=X, dy=0)` to position output rows**
4. **Chain components with `.right().length(spacing)`**
5. **Add explicit label offsets**

### Minimum Spacing Values:
- Between components: `.length(2)` or `dx=2`
- Label offset: `ofst=0.5`
- Font size: `fontsize=9`

**This approach combines the best of both worlds:**
- Absolute positioning for overall layout (via `move_from`)
- Automatic chaining for connections (via `.right()`, `.down()`)
- Explicit spacing control (via `.length()`)
- Clean label placement (via `ofst`, `loc`, `halign`)

---

## CONCLUSION

✅ **My original assumptions were PARTIALLY correct:**
- `.at()` does enable precise positioning
- Label `ofst` does prevent overlaps
- **BUT**: Chaining is NOT the problem - it's the STANDARD method!

❌ **What was ACTUALLY wrong:**
- Not storing elements in variables
- Not using anchors for branch positioning
- Not adding explicit spacing with `.length()`
- Not specifying label offsets

✅ **Correct approach for unified schematic:**
- Hybrid: Use `d.move_from()` for row positioning + chaining for connections
- Store M4 in variable for anchor access
- Add explicit `.length(2)` for spacing
- Use `ofst=0.5` for all labels
