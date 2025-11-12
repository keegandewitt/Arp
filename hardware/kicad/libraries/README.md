# KiCad Project Libraries

**Location:** `hardware/kicad/libraries/`
**Purpose:** Standard location for all custom/third-party KiCad libraries

---

## Current Libraries

### PJ-320A
- **Type:** 3.5mm audio jack connector
- **Source:** https://github.com/nathanhborger/PJ-320A_KiCad_Library
- **Files:**
  - Symbol: `PJ-320A/PJ-320A_Library.lib`
  - Footprint: `PJ-320A/PJ-320A_Library.pretty/`
- **Status:** ✅ Configured in sym-lib-table and fp-lib-table

---

## Adding New Libraries

**When you find a library you want to add:**

1. **Tell me:** "Add this library: [URL or name]"
2. **I will automatically:**
   - Clone/download to `hardware/kicad/libraries/[library-name]/`
   - Add symbol library to `sym-lib-table`
   - Add footprint library to `fp-lib-table`
   - Update this README
   - Commit to git

**You don't need to manually configure anything in KiCad!**

---

## How It Works

Libraries in this folder are automatically loaded via:
- `hardware/kicad/sym-lib-table` (symbol libraries)
- `hardware/kicad/fp-lib-table` (footprint libraries)

Both tables use `${KIPRJMOD}/libraries/...` paths, making them portable across machines.

---

## Using Libraries in KiCad

1. Open your KiCad project
2. Press `A` in schematic editor
3. Search for component (e.g., "PJ-320A")
4. Add to schematic
5. Assign footprint if needed

---

**Last Updated:** 2025-11-11
