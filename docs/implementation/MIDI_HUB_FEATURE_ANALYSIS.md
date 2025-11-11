# MIDI Hub Feature Analysis
## Competitive Feature Comparison for prisme Translation Hub

**Date:** 2025-11-01
**Status:** Research Phase
**Purpose:** Identify missing features from professional MIDI hubs/processors

---

## Research Sources

- **Blokas Midihub** - Stand-alone MIDI processor with 4×4 DIN ports + USB
- **Retrokits RK-006** - Ultra-portable 2×10 USB MIDI/Gate hub
- **iConnectivity mioXL** - Professional 8×12 DIN + 10 USB + network MIDI

---

## prisme Current Features ✓

### Translation Layers (Core Differentiator)
- ✅ **Scale Quantization** - 12 scales (Chromatic, Major, Minor, modes, Blues, Pentatonic)
- ✅ **Arpeggiator** - 16 patterns (Up, Down, UpDown, Random, etc.)
- ✅ **Clock Transformations** - Swing (50-75%), Multiply (1x/2x/4x), Divide (/1/2/4/8)

### Routing & I/O
- ✅ **Multiple Input Sources** - MIDI IN (DIN-5), USB MIDI, CV IN (planned), Gate IN (planned)
- ✅ **Input Router** - Select active source
- ✅ **Routing Modes** - THRU (pass-through) vs TRANSLATION (layer processing)
- ✅ **Real-time Pass-through** - Zero-latency for non-note MIDI messages
- ✅ **CV/Gate Output** - MCP4728 DAC for CV output
- ✅ **Custom CC Mapping** - MIDI CC → CV output with Learn Mode

### Clock & Sync
- ✅ **Dual Clock Sources** - Internal (30-300 BPM) or External
- ✅ **Clock Division** - Configurable step rate
- ✅ **Roger Linn Swing** - Industry-standard swing implementation
- ✅ **Clock Multiply/Divide** - Tempo scaling

### User Interface
- ✅ **OLED Display** - 128×64 with real-time status
- ✅ **3-Button Interface** - Pattern selection, settings, demo
- ✅ **Settings Menu** - 8 categories, hierarchical navigation
- ✅ **NVM Storage** - Persistent settings (35/256 bytes)

---

## Missing Features Analysis

### 🔴 HIGH PRIORITY - Core MIDI Processing

#### 1. **MIDI Channel Filtering/Remapping**
- **What it does:** Filter or remap MIDI channels (e.g., Ch 1 → Ch 10)
- **Use case:** Multi-timbral setups, channel isolation
- **Competitor:** Midihub (Channel Remap pipe), RK-006 (per-port filtering)
- **Implementation:** Easy - add channel filter to settings
- **Priority:** HIGH - fundamental MIDI routing feature

#### 2. **MIDI Merging**
- **What it does:** Combine multiple MIDI inputs into one output
- **Use case:** Multiple controllers to one synth
- **Competitor:** RK-006 (auto-merge in standalone), Midihub (Merge pipe)
- **Implementation:** Medium - already have multi-input routing, need merge logic
- **Priority:** HIGH - common use case for hubs
- **Note:** RK-006 has "auto-merge in standalone mode" for 2 MIDI IN ports

#### 3. **Note Transpose**
- **What it does:** Shift notes up/down by semitones
- **Use case:** Key changes, octave shifts
- **Competitor:** Midihub (Note Transpose pipe), universal feature
- **Implementation:** Easy - add to translation layers
- **Priority:** HIGH - extremely common feature

#### 4. **Velocity Curve/Remapping**
- **What it does:** Transform velocity values (fixed, curve, min/max)
- **Use case:** Keyboard sensitivity adjustment
- **Competitor:** Midihub (Velocity equalizer, sensitivity changer)
- **Implementation:** Easy - transform layer
- **Priority:** MEDIUM-HIGH - improves playability

### 🟡 MEDIUM PRIORITY - Creative Processing

#### 5. **Note to Chord**
- **What it does:** One note triggers multiple notes (chord)
- **Use case:** Instant harmonies, thick sounds
- **Competitor:** Midihub (Note to Chord pipe)
- **Implementation:** Medium - similar to arpeggiator logic
- **Priority:** MEDIUM - creative tool, less essential
- **Note:** Could integrate with existing arpeggiator system

#### 6. **MIDI Delay**
- **What it does:** Delay MIDI events by time or beats
- **Use case:** Echoes, generative patterns
- **Competitor:** Midihub (MIDI Delay pipe)
- **Implementation:** Medium - timing buffer needed
- **Priority:** MEDIUM - creative effect

#### 7. **Note Repeater**
- **What it does:** Repeat notes at clock rate
- **Use case:** Trills, rapid-fire notes
- **Competitor:** Midihub (Note Repeater pipe)
- **Implementation:** Medium - clock-synced note generation
- **Priority:** MEDIUM - similar to arpeggiator

#### 8. **CC LFO Generator**
- **What it does:** Generate CC values from LFO shapes
- **Use case:** Automated modulation, movement
- **Competitor:** Midihub (CC LFO pipe)
- **Implementation:** Hard - LFO engine needed
- **Priority:** MEDIUM - adds modulation capabilities

#### 9. **MIDI Randomizer**
- **What it does:** Randomize note, velocity, CC values
- **Use case:** Generative music, variation
- **Competitor:** Midihub (Randomizer pipe)
- **Implementation:** Easy-Medium - RNG with constraints
- **Priority:** MEDIUM - generative feature

### 🟢 LOW PRIORITY - Advanced Features

#### 10. **Fixed Note Length**
- **What it does:** Force all notes to specific duration
- **Use case:** Staccato/legato control
- **Competitor:** Midihub (Fixed Note Length pipe)
- **Implementation:** Easy - timer for note-off
- **Priority:** LOW - niche use case

#### 11. **Voice Dispatcher**
- **What it does:** Distribute notes across multiple channels (polyphony)
- **Use case:** Paraphonic synths, voice stealing
- **Competitor:** Midihub (Voice Dispatcher pipe)
- **Implementation:** Hard - voice management logic
- **Priority:** LOW - specialized feature

#### 12. **Keyboard Split**
- **What it does:** Different processing for note ranges
- **Use case:** Split keyboard zones
- **Competitor:** Midihub (Keyboard Splitter)
- **Implementation:** Medium - range-based routing
- **Priority:** LOW - can work around with external gear

#### 13. **MIDI Message Transformation**
- **What it does:** Convert message types (CC → Note, etc.)
- **Use case:** Creative routing, unusual mappings
- **Competitor:** Midihub (Transformer pipe)
- **Implementation:** Hard - message type conversion
- **Priority:** LOW - very advanced feature

#### 14. **Sustain Pedal Processing**
- **What it does:** Extend notes based on CC64
- **Use case:** Pedal-less sustain, creative holds
- **Competitor:** Midihub (Sustain Pedal pipe)
- **Implementation:** Medium - note hold logic
- **Priority:** LOW - hardware pedals exist

### 🔵 SYSTEM FEATURES

#### 15. **Multiple Presets/Scenes**
- **What it does:** Save/recall multiple configurations
- **Use case:** Different songs, quick setup changes
- **Competitor:** Midihub (8 presets), universal feature
- **Implementation:** Easy - NVM has space (221 bytes free)
- **Priority:** HIGH - workflow feature
- **Note:** Currently 35/256 bytes used, can store ~6 full presets

#### 16. **MIDI Learn Mode**
- **What it does:** Capture CC numbers for mapping
- **Use case:** Quick parameter assignment
- **Competitor:** Universal feature
- **Implementation:** Already exists for Custom CC!
- **Priority:** ✅ DONE - extend to other parameters?

#### 17. **Latency Monitoring**
- **What it does:** Measure/display processing latency
- **Use case:** Performance verification
- **Competitor:** Midihub (< 1.5ms spec)
- **Implementation:** Easy - timing measurement
- **Priority:** HIGH - user requested verification
- **Note:** USER REQUEST - verify no perceptible latency

---

## Performance Benchmarks

### Competitor Latency Specs
- **Blokas Midihub:** < 1.5ms MIDI loopback latency
- **Retrokits RK-006:** "Ultra fast MIDI handling" (no specific number)
- **prisme:** UNMEASURED - need to verify

### Our Hardware Limits
- **Platform:** Adafruit Feather M4 (SAMD51, 120MHz)
- **MIDI Baud Rate:** 31.25kbaud (320μs per byte)
- **Processing:** Python (CircuitPython) overhead
- **Estimate:** 1-3ms likely achievable, needs measurement

---

## Recommendations

### Phase 6 Additions (Before Documentation)

#### Must-Have Features
1. **Channel Filtering** - Essential routing feature (1-2 days)
2. **Note Transpose** - Universal expectation (1 day)
3. **Preset System** - Workflow improvement (2-3 days)
4. **Latency Test** - User requested, marketing value (1 day)

#### Nice-to-Have Features
5. **MIDI Merge** - Common use case (2-3 days)
6. **Velocity Curve** - Playability enhancement (1-2 days)

**Total Time Estimate:** 8-14 days for must-haves

### Future Roadmap (Post-v1.0)
- Note to Chord (integrate with arp system)
- MIDI Delay (creative effects)
- CC LFO Generator (modulation)
- Randomizer (generative music)

### Features We Don't Need
- Voice Dispatcher - Too niche
- Keyboard Split - Hardware exists
- Message Transformation - Over-complicated
- Sustain Pedal - Hardware solution preferred

---

## prisme's Unique Value Proposition

### What Makes Us Different

1. **Translation Hub Philosophy**
   - Not just routing - actual musical transformation
   - Fixed layer order (Scale → Arp → Clock) makes sense
   - CV/Gate output for hybrid setups

2. **Hardware Integration**
   - CV output via MCP4728 DAC
   - Custom CC → CV mapping with Learn Mode
   - OLED display with real-time feedback

3. **Focused Feature Set**
   - Not trying to be everything
   - Deep implementation of core features
   - Scale quantization + Arpeggiator combo is powerful

4. **Portability**
   - Compact Feather M4 platform
   - Battery-powered capability (future)
   - DAW-less setup friendly

### Competitive Positioning
- **vs Midihub:** More focused, better CV integration, lower cost
- **vs RK-006:** More processing power, translation layers, display
- **vs iConnectivity:** Portable, creative processing, not just routing

---

## User Request: Latency Verification

### Action Items
1. **Implement latency test mode**
   - Loopback MIDI IN → MIDI OUT timing
   - Display result on OLED
   - Test each translation layer individually

2. **Measure Critical Paths**
   - THRU mode latency (baseline)
   - Scale layer latency
   - Arp layer latency
   - Full pipeline latency
   - CV output latency

3. **Performance Targets**
   - **THRU mode:** < 1ms (should be near-instant)
   - **Translation mode:** < 3ms (human imperceptible threshold)
   - **CV output:** < 5ms (analog tolerant)

4. **Test Methodology**
   - External MIDI monitor with timestamps
   - Internal monotonic time measurements
   - Multiple message types (Note, CC, Clock)

### Documentation
- Add latency specs to README
- Create performance test suite
- Include in user manual

---

## Next Steps

1. ✅ **Complete Phase 5.6** - Display Redesign (DONE)
2. 🔄 **Evaluate Must-Have Features** - Discuss with user
3. ⏳ **Implement Selected Features** - Phase 6a
4. ⏳ **Latency Testing** - Phase 6b
5. ⏳ **Documentation** - Phase 6c
6. ⏳ **Hardware Testing** - Phase 7
7. ⏳ **Merge & Deploy** - Phase 8

---

## Questions for User

1. **Feature Priority:** Which missing features are most important?
   - Channel filtering?
   - Note transpose?
   - Preset system?
   - MIDI merge?

2. **Latency Testing:** Should we implement latency test mode in the device?

3. **Scope Creep:** Should we add features or focus on perfecting current ones?

4. **Documentation vs Features:** Prioritize writing docs or adding features first?

---

**Generated:** 2025-11-01
**Author:** the development environment (Session 16)
**Status:** Draft - Awaiting User Feedback
