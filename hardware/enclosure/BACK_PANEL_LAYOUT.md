# Back Panel Layout - Corrected Design

## Updated: 2025-11-02 - Fixed MIDI/LED Collisions (12mm offset for MIDI!)

### Panel Dimensions
- **Total Width: 120mm** (113mm internal + 2× 3.5mm walls)
- **Total Height: 72mm** (65mm internal + 2× 3.5mm walls)

### Component Positions (from left edge of panel)

#### BOTTOM ROW (15mm height from base)

| Component | X Position | Hole Size | Left Edge | Right Edge | Notes |
|-----------|-----------|-----------|-----------|------------|-------|
| USB-C     | 10mm      | 9.5×3.8mm | 5.25mm    | 14.75mm    | Rectangular cutout |
| CV OUT    | 22mm      | 6mm ø     | 19mm      | 25mm       | 1/8" jack |
| CV OUT LED| 29mm      | 3.2mm ø   | 27.4mm    | 30.6mm     | White LED |
| TRIG OUT  | 36mm      | 6mm ø     | 33mm      | 39mm       | 1/8" jack |
| TRIG OUT LED | 43mm   | 3.2mm ø   | 41.4mm    | 44.6mm     | RGB LED |
| CC OUT    | 50mm      | 6mm ø     | 47mm      | 53mm       | 1/8" jack |
| CC OUT LED| 57mm      | 3.2mm ø   | 55.4mm    | 58.6mm     | White LED |
| MIDI OUT  | 72mm      | 15.5mm ø  | 64.25mm   | 79.75mm    | 5-pin DIN |
| MIDI OUT LED | 84mm   | 3.2mm ø   | 82.4mm    | 85.6mm     | White LED (12mm offset!) |
| MIDI IN   | 96mm      | 15.5mm ø  | 88.25mm   | 103.75mm   | 5-pin DIN |
| MIDI IN LED | 108mm   | 3.2mm ø   | 106.4mm   | 109.6mm    | White LED (12mm offset!) |

#### TOP ROW (27mm height from base)

| Component | X Position | Hole Size | Left Edge | Right Edge | Notes |
|-----------|-----------|-----------|-----------|------------|-------|
| CV IN     | 22mm      | 6mm ø     | 19mm      | 25mm       | 1/8" jack |
| CV IN LED | 29mm      | 3.2mm ø   | 27.4mm    | 30.6mm     | White LED |
| TRIG IN   | 36mm      | 6mm ø     | 33mm      | 39mm       | 1/8" jack |
| TRIG IN LED | 43mm    | 3.2mm ø   | 41.4mm    | 44.6mm     | RGB LED |

### Clearance Verification

**BOTTOM ROW:**
- USB-C to CV OUT: 19mm - 14.75mm = **4.25mm ✓**
- CV OUT LED to TRIG OUT: 33mm - 30.6mm = **2.4mm ✓**
- TRIG OUT LED to CC OUT: 47mm - 44.6mm = **2.4mm ✓**
- CC OUT LED to MIDI OUT: 64.25mm - 58.6mm = **5.65mm ✓**
- MIDI OUT to MIDI OUT LED: 82.4mm - 79.75mm = **2.65mm ✓** (LED outside jack!)
- MIDI OUT LED to MIDI IN: 88.25mm - 85.6mm = **2.65mm ✓** (FIXED!)
- MIDI IN to MIDI IN LED: 106.4mm - 103.75mm = **2.65mm ✓** (LED outside jack!)
- MIDI IN LED to right edge: 120mm - 109.6mm = **10.4mm ✓**

**TOP ROW:**
- Left edge to CV IN: 19mm - 3.5mm (wall) = **15.5mm ✓**
- CV IN LED to TRIG IN: 33mm - 30.6mm = **2.4mm ✓**
- TRIG IN LED to right edge: 117mm - 44.6mm = **72.4mm ✓**

**All clearances ≥2.4mm minimum - NO COLLISIONS ✓**

### Visual Layout

```
BACK PANEL (view from outside looking at device)
═══════════════════════════════════════════════════════════════════════════════

TOP ROW (27mm):
                  ●   ●
                CV  TRIG
                IN   IN
                22   36mm

BOTTOM ROW (15mm):
    ▯     ●   ●   ●   ●   ●     ◯     ●     ◯     ●
   USB   CV TRIG CC                MIDI      MIDI
    C   OUT OUT OUT              OUT       IN
   10mm  22  36  50              72mm      96mm

═══════════════════════════════════════════════════════════════════════════════
Width: 120mm total (113mm internal + 7mm walls)

Legend:
  ● = 1/8" jack (6mm hole) + small LED dot (3.2mm) to the right
  ◯ = MIDI DIN (15.5mm large hole) + small LED dot (3.2mm) to the right
  ▯ = USB-C rectangular cutout
```

### Board Requirements

**FINAL PROTOBOARD SIZE: 108mm × 55mm**
- Cut from ElectroCookie 97mm × 89mm boards
- Requires 18mm more width than original 90mm design
- MIDI LEDs need 12mm offset (not 7mm!) to clear 15.5mm MIDI holes
- All jack positions measured from left edge of board (matching enclosure positions minus wall thickness)

### Assembly Notes

1. **Jack Alignment:** Jacks soldered to rear edge of protoboards at specified X positions
2. **LED Mounting:** LEDs press-fit into 3.2mm back panel holes, positioned 7mm right of jack centers
3. **Vertical Spacing:** 10mm M3 standoffs between INPUT/OUTPUT boards maintain 27mm/15mm heights
4. **MIDI Clearance:** Large 15.5mm DIN holes have adequate clearance from adjacent LEDs (>6.6mm)

**END OF LAYOUT**
