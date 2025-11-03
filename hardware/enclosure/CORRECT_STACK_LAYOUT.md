# CORRECT Stack Layout - Two Protoboard Design

## Updated: 2025-11-02 - FINAL CORRECT UNDERSTANDING

### Physical Stack Configuration

```
┌─────────────────────────────────────┐
│   OLED FeatherWing (128x64)         │  ← 7mm (1.6mm PCB + 5mm display/buttons)
│   Buttons A/B/C on LEFT side        │
└─────────────────────────────────────┘
         ↑ 10mm female headers
┌─────────────────────────────────────┐
│   Feather M4 Express                │  ← 8mm total height
│   (mounted on TOP board)            │
└─────────────────────────────────────┘
         ↑ 10mm standoffs
┌─────────────────────────────────────┐
│   TOP PROTOBOARD (108mm × 55mm)     │  ← 1.6mm PCB
│   - CV IN jack (left)               │
│   - TRIG IN jack (left)             │
│   - M4 mount points (center/right)  │
└─────────────────────────────────────┘
         ↑ 8mm board-to-board standoffs
┌─────────────────────────────────────┐
│   BOTTOM PROTOBOARD (108mm × 55mm)  │  ← 1.6mm PCB
│   - USB-C (far left)                │
│   - CV OUT, TRIG OUT, CC OUT (left) │
│   - MIDI FeatherWing (right)        │
│     • MIDI OUT DIN-5                │
│     • MIDI IN DIN-5                 │
└─────────────────────────────────────┘
         ↑ 4mm base
═════════════════════════════════════════
         ENCLOSURE BASE
```

### Height Calculation (Bottom to Top)

| Layer | Height | Running Total | Notes |
|-------|--------|---------------|-------|
| Base | 4.0mm | 4.0mm | Enclosure bottom |
| BOTTOM board PCB | 1.6mm | 5.6mm | All jacks mount THROUGH to back panel |
| Board-to-board standoff | 8.0mm | 13.6mm | M3 standoffs between boards |
| TOP board PCB | 1.6mm | 15.2mm | CV/TRIG IN jacks + M4 mount |
| Feather standoffs | 10.0mm | 25.2mm | M2.5 standoffs, M4 mounted on TOP board |
| Feather M4 | 8.0mm | 33.2mm | Complete Feather height with components |
| OLED standoffs | 10.0mm | 43.2mm | Female headers stack OLED on M4 |
| OLED FeatherWing | 7.0mm | 50.2mm | PCB + display + buttons |
| Top clearance | 2.0mm | **52.2mm** | Air gap |

**Rounded to: 50mm internal height** (tight but achievable with careful assembly)

### Back Panel Jack Layout

**BOTTOM ROW (jacks on BOTTOM board):**
- USB-C: 10mm
- CV OUT: 22mm (+ LED at 29mm)
- TRIG OUT: 36mm (+ LED at 43mm)
- CC OUT: 50mm (+ LED at 57mm)
- MIDI OUT: 72mm (+ LED at 84mm)
- MIDI IN: 96mm (+ LED at 108mm)

**TOP ROW (jacks on TOP board):**
- CV IN: 22mm (+ LED at 29mm)
- TRIG IN: 36mm (+ LED at 43mm)

All jacks soldered to rear edge of boards, going OUT through back panel.

### Component Positioning

**BOTTOM Board (108mm × 55mm):**
- **Left side (0-60mm):** USB-C, CV OUT, TRIG OUT, CC OUT jacks
- **Right side (60-108mm):** MIDI FeatherWing footprint
  - MIDI OUT DIN-5 jack at 72mm
  - MIDI IN DIN-5 jack at 96mm
  - Optoisolator and LEDs on board

**TOP Board (108mm × 55mm):**
- **Left side (0-50mm):** CV IN, TRIG IN jacks
- **Center/Right (50-108mm):** Feather M4 mount area
  - Feather positioned at ~60-110mm X
  - Clears CV/TRIG IN jacks
  - I2C/power connections to jacks

### OLED Position (in lid)

- **OLED cutout:** X=25mm, Y=5mm (left-justified)
- **Buttons A/B/C:** X=8mm, Y=5mm (LEFT of OLED - real FeatherWing layout!)
- **Button spacing:** 4.5mm vertical

### Final Dimensions

**Internal:** 113mm (W) × 50mm (D) × 50mm (H)
**External:** 120mm (W) × 57mm (D) × 56.5mm (H)

### Key Design Principles

1. **Two-board stack** with 8mm separation allows wiring between boards
2. **Feather M4 mounts ON TOP board**, not as separate layer
3. **MIDI FeatherWing components** on BOTTOM board (optoisolator, LEDs)
4. **All jacks go OUT the back**, not upward into enclosure
5. **OLED stack** on Feather uses standard female headers (10mm height)

**END OF CORRECT LAYOUT**
