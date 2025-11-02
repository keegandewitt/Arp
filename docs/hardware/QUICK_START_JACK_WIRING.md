# Quick Start: Jack Wiring

**Ready to wire the first output? Start here!**

---

## 🎯 Phase 1: CV Pitch Output (Easiest First)

**Time:** 15-20 minutes
**Difficulty:** ⭐⭐☆☆☆ (Easy)
**What you'll get:** 1V/octave CV pitch control for your synth

### What You Need

- [ ] 1× 1/8" (3.5mm) TS mono jack
- [ ] 2× Short wires (**RED** for signal/tip, **WHITE** for ground/sleeve)
- [ ] Multimeter
- [ ] Soldering iron + solder (if making permanent connections)
- [ ] Breadboard + jumpers (for temporary testing)

### Step 1: Locate MCP4728 Channel A Output

The MCP4728 DAC has 4 outputs. We want **Channel A**:

```
MCP4728 Breakout Board:
┌─────────────────────┐
│                     │
│  VOUTA ← Channel A  │ ← This one!
│  VOUTB              │
│  VOUTC              │
│  VOUTD              │
│  GND                │
│  VDD                │
│  SDA                │
│  SCL                │
└─────────────────────┘
```

### Step 2: Wire It Up

**Option A: Breadboard (Temporary Testing)**
1. Insert 1/8" jack into breadboard (or use alligator clips)
2. **RED** jumper wire: MCP4728 VOUTA → Jack TIP
3. **WHITE** jumper wire: MCP4728 GND → Jack SLEEVE
4. Done!

**Option B: Solder (Permanent)**
1. Solder **RED** wire to MCP4728 VOUTA pad
2. Solder **WHITE** wire to MCP4728 GND pad
3. Solder **RED** wire to jack TIP terminal
4. Solder **WHITE** wire to jack SLEEVE terminal
5. Use heat shrink or electrical tape for insulation

**Color Convention:** 🔴 RED = Tip (signal) | ⚪ WHITE = Sleeve (ground)

### Step 3: Verify Connections (POWER OFF!)

Use multimeter in continuity mode:

```bash
# Check signal path
Multimeter RED → MCP4728 VOUTA
Multimeter BLACK → Jack TIP
Result: Should BEEP (continuous connection)

# Check ground path
Multimeter RED → MCP4728 GND
Multimeter BLACK → Jack SLEEVE
Result: Should BEEP (continuous connection)

# Check for shorts
Multimeter RED → Jack TIP
Multimeter BLACK → Jack SLEEVE
Result: Should NOT beep (open circuit)
```

If all three checks pass → ✅ Ready to test!

### Step 4: Deploy Test Code

```bash
# Copy CV pitch test to device
cp tests/cv_1v_octave_test.py /Volumes/CIRCUITPY/code.py

# Watch serial output
python3 scripts/monitor_serial.py
```

### Step 5: Measure Voltages

Connect multimeter to the jack:
- **Red probe** → Jack TIP (red wire)
- **Black probe** → Jack SLEEVE (white wire)
- Set to **DC voltage**, 20V range

The test code will cycle through notes. Verify these voltages:

| Note | Expected Voltage |
|------|------------------|
| C0   | 1.00V ±0.05V |
| C1   | 2.00V ±0.05V |
| C2   | 3.00V ±0.05V |
| C3   | 4.00V ±0.05V |
| C4   | 5.00V ±0.05V |

**If voltages match** → ✅ **SUCCESS!** You have working CV output!

### Step 6: Test with Real Synth (Optional)

If you have a modular synth or hardware synth with CV input:

1. Connect jack to synth's **1V/octave pitch input**
2. The test code cycles through C0-C4
3. You should hear a chromatic scale going up in octaves
4. Each step should be exactly 1 octave apart

---

## 🎉 Success? Move to Phase 2!

Once CV Pitch is working, move on to:
- **Phase 2:** V-Trig Gate output (file: `gate_dual_output_test.py`)
- See full guide: `OUTPUT_JACKS_WIRING_GUIDE.md`

---

## 🔧 Troubleshooting

### No voltage at all
- Check MCP4728 is powered (VDD = 5V)
- Check I2C connection (run `tests/i2c_scan_mcp4728.py`)
- Verify wiring with continuity test

### Very low voltage (0.3V or less)
- **Bug in code:** Using `.value` instead of `.raw_value`
- Fix: All DAC code must use `dac.channel_a.raw_value = X`
- See: `docs/hardware/MCP4728_CV_GUIDE.md` section "The Value Property Trap"

### Voltage wrong but not zero
- Check MCP4728 reference voltage (should be Vref.VDD)
- Run `tests/mcp4728_correct_voltage_test.py` to reconfigure
- May need to call `dac.save_settings()` to persist config

### Voltage unstable/noisy
- Add 0.1µF ceramic capacitor between VDD and GND on MCP4728
- Check ground connection quality
- Ensure MCP4728 and M4 share common ground

---

## 📋 After Success

Once CV Pitch works:
- [ ] Take photo of breadboard setup
- [ ] Label the jack ("CV PITCH" or "1V/OCT")
- [ ] Mark task #1 as complete in todo list
- [ ] Move to Phase 2: V-Trig Gate output

**Congratulations!** You've successfully wired your first CV output! 🎊
