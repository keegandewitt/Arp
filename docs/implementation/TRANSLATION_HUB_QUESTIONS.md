# prisme Translation Hub - Critical Questions

**Created:** 2025-11-01 (Session 15)
**Purpose:** Identify and answer all uncertainties before implementation
**Status:** Questions identified, answers pending
**Target:** 95% confidence before coding

---

## Question 1: Which Architecture Foundation?

**Priority:** =4 BLOCKER

**The Question:**
Should we migrate to the class-based `Arpeggiator` in `arp/core/arpeggiator.py` or add translation layers to the inline system in `main.py`?

**Why It Matters:**
- Class-based already has scale quantization working (line 45)
- Class-based has 16 patterns vs inline's 5
- But migrating risks breaking a working system

**Options:**
1. **Migrate to class-based** - Clean foundation, scale quantization built-in, 4-6 hours
2. **Enhance inline** - Lower risk, but need to add scale quantization, 2-3 hours

**Research Needed:**
- Best practices for refactoring CircuitPython event loops
- Risk mitigation strategies for migration
- Testing approach for side-by-side comparison

**Answer:** (Pending research)

---

## Question 2: How to Handle USB MIDI Input for Notes?

**Priority:** =á HIGH

**The Question:**
Currently, USB MIDI is only used for clock input (`ClockHandler(midi_in_port=usb_midi.ports[0])`). How do we enable USB MIDI for note data when user selects USB as input source?

**Current Code:**
```python
# Line 137: USB only used for clock
clock = ClockHandler(midi_in_port=usb_midi.ports[0])

# Line 111-112: UART used for notes
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = MIDI(midi_in=uart, midi_out=uart)
```

**The Challenge:**
Can we have BOTH clock AND note input from USB simultaneously, or do we need separate MIDI objects?

**Research Needed:**
- CircuitPython USB MIDI architecture
- Can one MIDI object handle both clock and note messages?
- Do we need `usb_midi.ports[0]` and `usb_midi.ports[1]` for IN/OUT?

**Answer:** (Pending research)

---

## Question 3: Where to Insert Translation Layers?

**Priority:** =á HIGH

**The Question:**
At what point in the data flow should translation layers be applied?

**Options:**
1. **At input** (before note buffer):
   ```
   NoteOn ’ Quantize ’ Add to buffer ’ Arpeggiate ’ Output
   ```
   - Pro: Notes stored already quantized
   - Con: Can't do Arp ’ Scale ordering

2. **At output** (after arpeggiator generates sequence):
   ```
   NoteOn ’ Add to buffer ’ Arpeggiate ’ Quantize ’ Output
   ```
   - Pro: Supports both Scale ’ Arp and Arp ’ Scale
   - Con: Need to quantize every step

3. **Configurable** (based on user's layer order setting):
   ```
   If Scale First: Quantize at input
   If Arp First: Quantize at output
   ```
   - Pro: True user-definable ordering
   - Con: More complex logic

**Research Needed:**
- Event-driven architecture patterns for transformation pipelines
- Performance impact of quantizing on every step

**Answer:** (Pending research)

---

## Question 4: Swing Implementation Details

**Priority:** =â MEDIUM

**The Question:**
How exactly should swing be implemented at the clock tick level?

**Current Understanding:**
- Swing delays every 2nd 16th note by X% of the tick interval
- Formula: `delay_ms = (tick_interval * swing_percent / 100)`

**Uncertainties:**
1. Do we delay the tick itself, or the note output?
2. Does swing apply to internal clock only, or external too?
3. How do we prevent drift accumulation?
4. What if swing makes ticks overlap?

**Research Needed:**
- Swing implementation in hardware sequencers
- Drift compensation with swing enabled
- CircuitPython timing precision with `time.sleep()`

**Answer:** (Pending research)

---

## Question 5: Clock Multiply/Divide Math

**Priority:** =â MEDIUM

**The Question:**
How do we implement tempo multiply and divide without breaking the clock system?

**Current Clock System:**
```python
# Lines 58-69: Internal tick interval calculation
def _calculate_tick_interval(self, bpm):
    """24 ticks per quarter note, 60 seconds per minute"""
    return 60.0 / (bpm * 24)
```

**For Multiply (2x):**
- Option A: Halve the tick interval (faster ticks)
- Option B: Send 2 ticks for every 1 received
- Option C: Double the BPM value

**For Divide (1/2):**
- Option A: Double the tick interval (slower ticks)
- Option B: Send 1 tick for every 2 received
- Option C: Halve the BPM value

**Which approach is correct?**

**Research Needed:**
- MIDI clock multiplication/division standards
- How DAWs implement clock scaling
- Impact on external clock source (can we modify external clock?)

**Answer:** (Pending research)

---

## Question 6: How to Apply Clock Transformations?

**Priority:** =â MEDIUM

**The Question:**
Do clock transformations (swing, multiply, divide) apply to the clock BEFORE or AFTER it reaches the arpeggiator?

**Options:**
1. **Transform at clock source:**
   ```
   Clock source ’ Apply multiply/divide/swing ’ Send to arpeggiator
   ```
   - Pro: Arpeggiator receives already-transformed clock
   - Con: Need to modify `ClockHandler`

2. **Transform at arpeggiator:**
   ```
   Clock source ’ Raw clock ’ Arpeggiator applies transformations
   ```
   - Pro: Clock handler stays simple
   - Con: Mixing concerns (arpeggiator shouldn't know about clock)

**Research Needed:**
- Separation of concerns in clock systems
- Where do professional devices apply swing?

**Answer:** (Pending research)

---

## Question 7: CV IN Voltage Reading (ADC Setup)

**Priority:** =5 LOW (Future)

**The Question:**
How do we read analog voltage from CV IN on the SAMD51?

**Requirements:**
- Read 0-10V input (modular CV range)
- M4's ADC only reads 0-3.3V
- Need voltage divider circuit (scale 0-10V ’ 0-3.3V)

**Uncertainties:**
1. Which ADC pin to use? (A2 suggested in architecture)
2. ADC resolution? (SAMD51 has 12-bit ADC)
3. How to configure ADC in CircuitPython?
4. Voltage divider resistor values?
5. Protection diodes needed?

**Research Needed:**
- CircuitPython ADC setup for SAMD51
- Voltage divider design for 0-10V ’ 0-3.3V
- Input protection best practices

**Answer:** (Pending research - but deprioritized for now)

---

## Question 8: Gate IN Protection Circuit

**Priority:** =5 LOW (Future)

**The Question:**
How do we safely read 5V or 12V gate signals on a 3.3V-tolerant GPIO pin?

**Requirements:**
- Gate signals: 5V (Eurorack) or 12V (vintage modular)
- M4 GPIO: 3.3V maximum (damage above this!)
- Need voltage protection

**Circuit Options:**
1. **Voltage divider** (10k© + 22k©): Scales 12V ’ 3.1V
2. **Schmitt trigger buffer** (74HC14): Clean gate with hysteresis
3. **Optocoupler**: Complete isolation (overkill?)

**Uncertainties:**
1. Which GPIO pin? (D4 suggested in architecture)
2. Can we use internal pull-down, or need external?
3. Diode clamp needed even with voltage divider?

**Research Needed:**
- GPIO protection circuits for SAMD51
- Schmitt trigger vs voltage divider trade-offs

**Answer:** (Pending research - but deprioritized for now)

---

## Question 9: Refactor Strategy - New File or In-Place?

**Priority:** =á HIGH

**The Question:**
Should we create `main_v2.py` for the new architecture, or refactor `main.py` in-place?

**Options:**
1. **Create main_v2.py:**
   -  Keep working system intact
   -  Easy to test side-by-side
   -  Can rollback instantly
   - L Need to manually switch later
   - L Two files to maintain during transition

2. **Refactor main.py in-place:**
   -  No file switching needed
   -  Single source of truth
   - L Risk of breaking working system
   - L Harder to rollback

3. **Feature branch + main_v2.py:**
   -  Best of both worlds
   -  Git allows easy comparison
   -  Can test thoroughly before merging
   - L More git complexity

**Research Needed:**
- Best practices for refactoring embedded systems
- Risk mitigation for production code changes

**Answer:** (Pending research)

---

## Question 10: Testing Strategy

**Priority:** =á HIGH

**The Question:**
How do we verify that translation layers work correctly without breaking existing functionality?

**What Needs Testing:**
1. **Thru mode:** All MIDI passes through unchanged
2. **Scale ’ Arp:** Notes quantized before arpeggiation
3. **Arp ’ Scale:** Notes arpeggiated first, then quantized
4. **Layer enable/disable:** Layers can be toggled independently
5. **Input source switching:** MIDI IN, USB work correctly
6. **Output verification:** All outputs (MIDI, USB, CV, Gate, CC) still work
7. **Clock transformations:** Swing, multiply, divide work as expected

**Testing Approach:**
- Unit tests? (CircuitPython doesn't have pytest)
- Hardware tests? (deploy to device, manual verification)
- Comparison tests? (main.py vs main_v2.py side-by-side)

**Research Needed:**
- CircuitPython testing strategies
- Hardware-in-the-loop test approaches

**Answer:** (Pending research)

---

## Summary of Questions

**BLOCKERS (Must answer before starting):**
- Q1: Which architecture foundation?

**HIGH PRIORITY (Answer before implementation):**
- Q2: USB MIDI input for notes
- Q3: Where to insert translation layers
- Q9: Refactor strategy
- Q10: Testing strategy

**MEDIUM PRIORITY (Can answer during implementation):**
- Q4: Swing implementation details
- Q5: Clock multiply/divide math
- Q6: Clock transformation application point

**LOW PRIORITY (Future features):**
- Q7: CV IN voltage reading (not in MVP)
- Q8: Gate IN protection (not in MVP)

---

**Next Step:** Research and answer questions using Perplexity MCP

**Target:** 95% confidence ’ Implement!
