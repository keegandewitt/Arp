# PRISME Project Standards

**Date:** 2025-11-11
**Purpose:** Single reference for formatting, orientation, and design standards

---

## KiCad Schematic Standards

**Paper Size:** A4
**Orientation:** Portrait (default for `paper "A4"` in KiCad)
**Version:** KiCad 9.0

**Schematic File Reference:**
```
(kicad_sch
	(version 20250114)
	(generator "eeschema")
	(generator_version "9.0")
	(paper "A4")
```

**Rule:** All schematics MUST use A4 portrait unless explicitly changed for specific need.

---

## Documentation Standards

**Format:** Markdown (.md)
**Line Length:** No hard limit (readability first)
**Headers:** ATX style (# ## ###)
**Code Blocks:** Use triple backticks with language identifier

---

## Component Verification Workflow

**Before adding any component, verify:**

1. **Symbol exists** in KiCad standard libraries OR imported libraries
2. **Footprint exists** and matches physical component
3. **3D model** available (optional but preferred)
4. **Cross-reference** minimum 2 sources:
   - KiCad standard library
   - Adafruit Eagle imports
   - SnapEDA/UltraLibrarian
   - Manufacturer datasheets

**Multi-Point Verification:**
- Use MCP tools to search 3+ sources
- Compare symbol pinouts across sources
- Verify footprint dimensions against datasheet
- Check for community-reported issues

---

## File Creation Standards

**NEVER create files without:**
1. Checking existing project files for formatting
2. Verifying orientation/paper size matches project standard
3. Reading at least 2 existing similar files as reference
4. Confirming with user if any ambiguity exists

**ALWAYS:**
- Read existing files BEFORE creating new ones
- Match existing patterns and conventions
- Ask user for clarification if standards conflict

---

## Component Library Locations

**Standard KiCad Libraries:**
- Device (resistors, caps, LEDs)
- Transistor_BJT (2N3904, etc.)
- Diode (BAT85, etc.)
- Isolator (6N138 optocoupler)
- Connector_Audio (3.5mm jacks)
- Connector (DIN, headers, etc.)

**Project Libraries (hardware/kicad/libraries/):**
- **THIS IS THE STANDARD LOCATION FOR ALL CUSTOM LIBRARIES**
- PJ-320A: 3.5mm audio jack (symbol + footprint)
- Add any new custom libraries here
- Automatically loaded via sym-lib-table and fp-lib-table

**Adafruit Libraries (Global):**
- `/Users/keegandewitt/Documents/KiCad/Adafruit_3D_Models/` (3D models)
- `/Users/keegandewitt/Documents/KiCad/Adafruit_Eagle_Library/` (Eagle files)

**Project Eagle Imports (hardware/kicad/eagle_imports/):**
- MCP4728: Available in `eagle_imports/mcp4728/`
- USB-C 4090: Available in `eagle_imports/usb_c_4090/`
- `Prisme-eagle-import.kicad_sym` (converted symbols in root)

**Adding New Libraries:**
1. Clone/download library to `hardware/kicad/libraries/[library-name]/`
2. Edit `hardware/kicad/sym-lib-table` to add symbol library
3. Edit `hardware/kicad/fp-lib-table` to add footprint library
4. Commit to git (libraries are part of project)
5. Use `${KIPRJMOD}/libraries/...` for portable paths

---

## Git Commit Standards

**Commit messages:**
- Use conventional commits format (feat:, fix:, refactor:, docs:)
- Include Claude Code attribution footer
- Be descriptive but concise

**Before committing:**
- Verify no .DS_Store files
- Check for embedded .git repos (cause submodule issues)
- Test that files actually work

---

## Design Philosophy

From ACTUAL_HARDWARE_TRUTH.md:

**Keep it simple:**
- Don't over-engineer
- Start with what actually works
- Add protection where critical (inputs)
- Skip unnecessary complexity (no op-amp if 0-5V works)
- Document reality, not aspirations

**Trust but verify:**
- User's breadboard is ground truth
- Documentation can be wrong
- Always multi-point verify before believing docs
- Cross-check against physical hardware

---

## Error Prevention Checklist

**Before creating any schematic/diagram:**
- [ ] Check existing project files for paper size
- [ ] Verify orientation matches `Prisme.kicad_sch` (A4 portrait)
- [ ] Read at least one similar existing file
- [ ] Confirm component symbols are available
- [ ] Multi-point verify component details if uncertain

**Before creating any documentation:**
- [ ] Check similar docs for formatting
- [ ] Verify information against multiple sources
- [ ] Mark speculative content as "planned" not "built"
- [ ] Distinguish between current design and future upgrades

---

**Status:** ACTIVE
**Last Updated:** 2025-11-11
**Reference:** hardware/docs/PROJECT_STANDARDS.md
