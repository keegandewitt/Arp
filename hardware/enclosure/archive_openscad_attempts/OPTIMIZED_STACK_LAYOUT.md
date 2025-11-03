# Optimized 2-Board Stack Layout

## Updated: 2025-11-02 - Ultra-Compact Design with Feather Over MIDI Area

### Key Innovation: Feather M4 Stack Positioned Over MIDI Jacks

Instead of a traditional 4-board vertical stack, this design uses a **2-board layout** where the Feather M4 + OLED FeatherWing stack is mounted horizontally on the INPUT board, positioned directly above the MIDI jack area on the OUTPUT board below.

### Space Analysis

**INPUT Board Jack Layout (108mm × 55mm):**
- LEFT side (X: 0-50mm): CV IN (22mm), TRIG IN (36mm)
- RIGHT side (X: 50-108mm): **COMPLETELY OPEN** - perfect for Feather placement!

**Feather M4 Dimensions:** 50.8mm × 22.8mm × 7mm
**OLED FeatherWing:** 50.9mm × 22.9mm × ~5mm (display height)

**Available Space:** 58mm width from X=50mm to X=108mm → Feather fits perfectly!

### Stack Configuration (Bottom to Top)

```
                    ┌─────────────────┐
                    │  OLED Display   │  ← Top (visible through lid cutout)
                    │  (Buttons Left) │
                    └─────────────────┘
                         ↑ 6mm standoff
                    ┌─────────────────┐
                    │  Feather M4     │
                    │  + MIDI Wing    │
                    └─────────────────┘
                         ↑ 8mm standoff
  ┌──────────────────────────────────────┐
  │  INPUT BOARD (108mm × 55mm)          │
  │  CV IN  TRIG IN    [Feather mounts→]│  ← Feather positioned over MIDI area
  │  (22mm) (36mm)                        │
  └──────────────────────────────────────┘
                ↑ 6mm standoff
  ┌──────────────────────────────────────┐
  │  OUTPUT BOARD (108mm × 55mm)         │
  │  USB CV TRIG CC    MIDI   MIDI       │  ← MIDI jacks directly below Feather!
  │  (10)(22)(36)(50)  OUT    IN         │
  │                   (72mm) (96mm)      │
  └──────────────────────────────────────┘
                ↑ Base (4mm)
  ════════════════════════════════════════
                ENCLOSURE BASE
```

### Height Calculation

| Component | Height | Running Total | Notes |
|-----------|--------|---------------|-------|
| Base thickness | 4.0mm | 4.0mm | Enclosure bottom |
| OUTPUT board PCB | 1.6mm | 5.6mm | With jacks through back panel |
| Standoff #1 | 6.0mm | 11.6mm | Minimum for solder joint clearance |
| INPUT board PCB | 1.6mm | 13.2mm | Feather mounts on top of this |
| Feather standoff | 8.0mm | 21.2mm | Standard Feather stacking height |
| Feather M4 + MIDI Wing | 8.6mm | 29.8mm | 1.6mm PCB + 7mm component height |
| OLED standoff | 6.0mm | 35.8mm | Aggressive minimum spacing |
| OLED FeatherWing | 6.6mm | 42.4mm | 1.6mm PCB + 5mm display |
| Top clearance | 2.0mm | **44.4mm** | Air gap |

**Internal Height Required: 45mm** (44.4mm rounded up)

**External Height: 45mm + 4mm (base) + 5.5mm (lid) = 54.5mm total**

### Benefits of This Design

1. **Reduced Height**: Saves ~5-10mm vs. separate 4-board stack
2. **Better Weight Distribution**: Feather mass positioned centrally over MIDI area
3. **Shorter Wiring**: I2C connections between Feather and INPUT board jacks are minimal
4. **Mechanical Stability**: Feather anchored to same board as CV/TRIG inputs
5. **Thermal**: Vertical air circulation around Feather between two boards

### Physical Mounting Details

**Feather M4 Position on INPUT Board:**
- X position: ~60mm from left edge (centered over MIDI area)
- Y position: 15mm from front edge (centered on 55mm board)
- Mounted with 4× M2.5 or M3 standoffs (8mm height)

**OLED FeatherWing Position:**
- Stacked on Feather using standard female headers
- OLED display cutout in lid at: X=25mm, Y=5mm (left-justified)
- Buttons A/B/C accessible through lid at: X=8mm, Y=5-14mm

### Assembly Order

1. Solder all jacks to OUTPUT board (rear edge)
2. Mount OUTPUT board to enclosure base with M3 screws
3. Install 6mm standoffs on OUTPUT board (4 corners)
4. Solder CV IN and TRIG IN jacks to INPUT board (rear edge, left side)
5. Install 8mm standoffs for Feather on INPUT board (right side, over MIDI area)
6. Mount Feather M4 + MIDI Wing to standoffs
7. Stack OLED FeatherWing on Feather (with 6mm standoffs or female headers)
8. Lower INPUT board assembly onto OUTPUT board standoffs
9. Wire I2C, power, and signals between boards
10. Secure INPUT board with M3 screws
11. Close lid

### Enclosure Dimensions

**Internal:** 113mm (W) × 50mm (D) × 45mm (H)
**External:** 120mm (W) × 57mm (D) × 54.5mm (H)

**Volume Reduction vs. Original Design:**
- Original: 120 × 72 × 66.5mm = 574,560 mm³
- Optimized: 120 × 57 × 54.5mm = 372,780 mm³
- **35% volume reduction!**

### Critical Success Factors

✓ **Feather positioned at X=60-110mm** (clears CV/TRIG jacks at 22mm/36mm)
✓ **8mm Feather standoffs minimum** (allows I2C wiring underneath)
✓ **6mm board-to-board standoffs** (clears solder joints)
✓ **MIDI jacks mount through back panel** (don't protrude upward into enclosure)
✓ **OLED left-justified** (minimizes enclosure depth to 50mm)

**END OF OPTIMIZED LAYOUT**
