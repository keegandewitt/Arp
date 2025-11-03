// ============================================================================
// PRISME Translation Hub - Parametric Enclosure with LED Indicators
// ============================================================================
// 3D-printable enclosure for Feather M4 + OLED + MCP4728 CV/Gate I/O + LEDs
// Designed for semi-transparent PLA filament (prism effect)
//
// Updated: 2025-11-02 - Added 7 LED indicator holes
//
// Usage:
//   - Adjust dimensions in CONFIGURATION section
//   - Set render_part to show: "preview", "box", "lid", or "both"
//   - Generate STL: F6 (Render) then F7 (Export STL)
// ============================================================================

// ============================================================================
// CONFIGURATION
// ============================================================================

// What to render (change this for different views/exports)
render_part = "preview"; // Options: "preview", "box", "lid", "both"

// === ENCLOSURE DIMENSIONS ===
// Internal dimensions (clearance for components)
// 2-BOARD STACK: BOTTOM (USB+CV OUT+TRIG OUT+CC OUT+MIDI Wing) + TOP (CV IN+TRIG IN+M4+OLED)
internal_width = 113;   // X-axis (left-right) - MIDI spacing needs proper clearance!
internal_depth = 50;    // Y-axis (front-back) - LEFT-JUSTIFIED OLED
internal_height = 50;   // Z-axis (bottom-top) - Two boards + M4 + OLED stack

// Wall thicknesses (optimized for semi-transparent PLA)
wall_thickness = 3.5;   // Side walls (strong enough for transparent filament)
base_thickness = 4;     // Bottom (extra strength for rubber feet)
top_thickness = 2.5;    // Top (thin for prism effect, supported by screws)

// Corner radius (rounded edges for professional look)
corner_radius = 2;      // 2mm radius

// === ASSEMBLY FEATURES ===
// Lid lip (creates recessed area for lid to nest)
lip_height = 3;         // How deep lid sits into box
lip_width = 2;          // Inset from wall edge
lid_tolerance = 0.2;    // Clearance for 3D printing fit (0.2mm works for PLA)

// Screw posts (M3 countersunk screws)
screw_post_diameter = 6;        // Base diameter of post
screw_hole_diameter = 3.2;      // M3 clearance hole (3.2mm for easy fit)
screw_head_diameter = 6.5;      // Countersink for M3 flat head
screw_head_depth = 2;           // Countersink depth
screw_post_inset = 8;           // Distance from corner to post center

// === BACK PANEL - JACK LAYOUT ===
// All positions match PROTOBOARD_LAYOUT.md rear edge measurements
// Layout: TOP ROW (2 jacks), BOTTOM ROW (6 jacks + USB-C)

// 1/8" (3.5mm) mono jacks - CV and Gate I/O
jack_hole_diameter = 6.0;       // 1/8" jack hole (6mm for panel mount)
jack_spacing_standard = 12;     // 12mm center-to-center spacing (comfortable patching)

// 5-pin DIN MIDI panel mount
midi_connector_diameter = 15.5; // 5-pin DIN panel mount hole (15mm + tolerance)
midi_spacing = 20;              // 20mm center-to-center spacing (MIDI standard)

// USB-C panel mount cutout
usb_width = 9.5;                // USB-C connector width (9mm + tolerance)
usb_height = 3.8;               // USB-C connector height (3.5mm + tolerance)

// LED indicators (flat-top 3mm LEDs)
led_hole_diameter = 3.2;        // 3mm LED + tolerance (flat-top style)
led_offset_from_jack = 7;       // 7mm to the right of small jack centers (1/8" jacks)
led_offset_from_midi = 12;      // 12mm to the right of MIDI jack centers (clears 15.5mm hole!)

// === JACK POSITIONS (measured from left edge of back panel) ===
// NEW LAYOUT based on 2025-11-02 design with LED indicators:
//
// TOP ROW (INPUT board - 2 jacks):     CV IN, TRIG IN
// BOTTOM ROW (OUTPUT board - 6 jacks): USB-C, CV OUT, TRIG OUT, CC OUT, MIDI OUT, MIDI IN
//
// All measurements from enclosure LEFT edge (including wall thickness)

// Y positions (height from enclosure base):
bottom_row_y = 15;                     // OUTPUT board jacks height (BOTTOM ROW)
top_row_y = 27;                        // INPUT board jacks height (TOP ROW)

// X positions (from left edge of enclosure, including wall offset):
// BOTTOM ROW (OUTPUT board - left to right):
// CORRECTED 2025-11-02: Proper clearances to avoid LED/MIDI collisions
usb_c_x = 10;                          // USB-C near left edge
cv_out_x = 22;                         // CV OUT
trig_out_x = 36;                       // TRIG OUT (14mm spacing for LED clearance)
cc_out_x = 50;                         // CC OUT (14mm spacing for LED clearance)
midi_out_x = 72;                       // MIDI OUT (22mm gap for LED + MIDI clearance)
midi_in_x = 96;                        // MIDI IN (24mm spacing for proper LED clearance)

// TOP ROW (INPUT board - aligned with BOTTOM):
cv_in_x = 22;                          // CV IN (aligned with CV OUT)
trig_in_x = 36;                        // TRIG IN (aligned with TRIG OUT)

// LED positions (7mm for small jacks, 12mm for MIDI jacks):
cv_in_led_x = cv_in_x + led_offset_from_jack;        // 29mm
trig_in_led_x = trig_in_x + led_offset_from_jack;    // 43mm
cv_out_led_x = cv_out_x + led_offset_from_jack;      // 29mm
trig_out_led_x = trig_out_x + led_offset_from_jack;  // 43mm
cc_out_led_x = cc_out_x + led_offset_from_jack;      // 57mm
midi_out_led_x = midi_out_x + led_offset_from_midi;  // 84mm (12mm offset!)
midi_in_led_x = midi_in_x + led_offset_from_midi;    // 108mm (12mm offset!)

// === TOP PANEL - OLED AND BUTTONS ===
// OLED cutout (128x64 SH1107 display)
oled_width = 30;                // Display visible area width
oled_height = 16;               // Display visible area height
oled_offset_x = 25;             // From left edge (buttons are to the LEFT on real hardware!)
oled_offset_y = 5;              // From front edge (LEFT-JUSTIFIED for compact depth!)

// Button holes (OLED FeatherWing: A, B, C)
// Real FeatherWing has buttons on the LEFT side of OLED!
button_diameter = 6.5;          // 6mm tactile button + tolerance
button_spacing = 4.5;           // Spacing between button centers (compact on real board)
buttons_offset_x = 8;           // From left edge (BUTTONS LEFT OF OLED - real layout!)
buttons_offset_y = 5;           // From front edge (LEFT-JUSTIFIED with OLED!)

// === VENTILATION ===
vent_slot_width = 1.5;          // Slot width
vent_slot_length = 20;          // Slot length
vent_slot_spacing = 5;          // Spacing between slots

// ============================================================================
// CALCULATED DIMENSIONS (DO NOT EDIT)
// ============================================================================

// External dimensions
external_width = internal_width + (wall_thickness * 2);
external_depth = internal_depth + (wall_thickness * 2);
box_external_height = internal_height + base_thickness;
lid_external_height = top_thickness + lip_height;
total_height = box_external_height + lid_external_height;

// ============================================================================
// MAIN RENDERING LOGIC
// ============================================================================

if (render_part == "preview") {
    // Show box and lid together for visualization (dark colors for visibility)
    translate([0, 0, box_external_height + 2])
        color("dimgray", 0.9) lid();
    color("slategray", 0.9) box();
} else if (render_part == "box") {
    box();
} else if (render_part == "lid") {
    lid();
} else if (render_part == "both") {
    // Print layout: box and lid side-by-side
    box();
    translate([external_width + 10, 0, 0])
        lid();
}

// ============================================================================
// BOX MODULE
// ============================================================================

module box() {
    difference() {
        // Main box body with rounded corners
        rounded_box(external_width, external_depth, box_external_height, corner_radius);

        // Hollow out interior
        translate([wall_thickness, wall_thickness, base_thickness])
            cube([internal_width, internal_depth, internal_height + 10]);

        // Create lip recess for lid
        translate([wall_thickness + lip_width,
                   wall_thickness + lip_width,
                   box_external_height - lip_height])
            cube([internal_width - (lip_width * 2),
                  internal_depth - (lip_width * 2),
                  lip_height + 1]);

        // Back panel cutouts (jacks + USB-C + MIDI + LEDs)
        back_panel_cutouts();

        // Side ventilation slots
        ventilation_slots();

        // Screw holes (pass-through for box)
        screw_holes_box();
    }

    // Add screw posts
    screw_posts();
}

// ============================================================================
// LID MODULE
// ============================================================================

module lid() {
    difference() {
        // Main lid body
        union() {
            // Top plate
            rounded_box(external_width, external_depth, top_thickness, corner_radius);

            // Lip that fits into box
            translate([wall_thickness + lip_width + lid_tolerance,
                       wall_thickness + lip_width + lid_tolerance,
                       top_thickness])
                rounded_box(internal_width - (lip_width * 2) - (lid_tolerance * 2),
                           internal_depth - (lip_width * 2) - (lid_tolerance * 2),
                           lip_height,
                           corner_radius - lip_width);
        }

        // OLED cutout
        translate([oled_offset_x + wall_thickness,
                   oled_offset_y + wall_thickness,
                   -1])
            cube([oled_width, oled_height, top_thickness + 2]);

        // Button holes
        for (i = [0:2]) {
            translate([buttons_offset_x + wall_thickness,
                       buttons_offset_y + wall_thickness + (i * button_spacing),
                       -1])
                cylinder(h = top_thickness + 2, d = button_diameter, $fn = 30);
        }

        // Screw holes (countersunk for lid)
        screw_holes_lid();
    }
}

// ============================================================================
// BACK PANEL CUTOUTS
// ============================================================================
//
// LAYOUT (2025-11-02 definitive design with LED indicators):
//
// TOP ROW (INPUT board - 27mm height):
//   - 2� 1/8" jacks: CV IN, TRIG IN
//   - 2� LED holes: white (CV IN), RGB (TRIG IN)
//
// BOTTOM ROW (OUTPUT board - 15mm height):
//   - 1� USB-C cutout
//   - 4� 1/8" jacks: CV OUT, TRIG OUT, CC OUT
//   - 2� MIDI DIN jacks: MIDI OUT, MIDI IN
//   - 5� LED holes: white (CV OUT, CC OUT, MIDI�2), RGB (TRIG OUT)
//
// MOUNTING METHOD:
//   - All 1/8" jacks soldered to protoboard rear edges
//   - MIDI DIN jacks panel-mount (threaded bushing)
//   - USB-C panel-mount breakout
//   - LEDs press-fit into 3.2mm holes (flat-top 3mm LEDs)
//   - Metal standoffs ensure jack alignment
//
// ============================================================================

module back_panel_cutouts() {
    // Rotate 90� and position at back panel
    // All positions measured from enclosure left edge + base
    rotate([90, 0, 0])
    translate([0, 0, -1]) {

        // === TOP ROW - INPUT BOARD JACKS (2 jacks + 2 LEDs) ===

        // CV IN jack (1/8" mono)
        translate([cv_in_x, top_row_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // CV IN LED (white)
        translate([cv_in_led_x, top_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // TRIG IN jack (1/8" mono)
        translate([trig_in_x, top_row_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // TRIG IN LED (RGB)
        translate([trig_in_led_x, top_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // === BOTTOM ROW - OUTPUT BOARD JACKS (6 connectors + 5 LEDs) ===

        // USB-C panel mount (rectangular cutout, no LED)
        translate([usb_c_x - (usb_width / 2),
                   bottom_row_y - (usb_height / 2),
                   0])
            cube([usb_width, usb_height, wall_thickness + 2]);

        // CV OUT jack (1/8" mono)
        translate([cv_out_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // CV OUT LED (white)
        translate([cv_out_led_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // TRIG OUT jack (1/8" mono)
        translate([trig_out_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // TRIG OUT LED (RGB)
        translate([trig_out_led_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // CC OUT jack (1/8" mono)
        translate([cc_out_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // CC OUT LED (white)
        translate([cc_out_led_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // MIDI OUT jack (5-pin DIN panel mount)
        translate([midi_out_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = midi_connector_diameter, $fn = 40);

        // MIDI OUT LED (white)
        translate([midi_out_led_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);

        // MIDI IN jack (5-pin DIN panel mount)
        translate([midi_in_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = midi_connector_diameter, $fn = 40);

        // MIDI IN LED (white)
        translate([midi_in_led_x, bottom_row_y, 0])
            cylinder(h = wall_thickness + 2, d = led_hole_diameter, $fn = 20);
    }
}

// ============================================================================
// VENTILATION SLOTS
// ============================================================================

module ventilation_slots() {
    // Left side vents
    for (i = [0:3]) {
        translate([-1,
                   wall_thickness + 20 + (i * vent_slot_spacing * 2),
                   base_thickness + 10])
            rotate([0, 90, 0])
                rounded_slot(vent_slot_width, vent_slot_length, wall_thickness + 2);
    }

    // Right side vents
    for (i = [0:3]) {
        translate([external_width + 1,
                   wall_thickness + 20 + (i * vent_slot_spacing * 2),
                   base_thickness + 10])
            rotate([0, -90, 0])
                rounded_slot(vent_slot_width, vent_slot_length, wall_thickness + 2);
    }
}

// ============================================================================
// SCREW POSTS AND HOLES
// ============================================================================

module screw_posts() {
    // Four corner posts
    post_positions = [
        [screw_post_inset, screw_post_inset],
        [external_width - screw_post_inset, screw_post_inset],
        [screw_post_inset, external_depth - screw_post_inset],
        [external_width - screw_post_inset, external_depth - screw_post_inset]
    ];

    for (pos = post_positions) {
        translate([pos[0], pos[1], base_thickness])
            cylinder(h = internal_height - lip_height,
                    d = screw_post_diameter,
                    $fn = 30);
    }
}

module screw_holes_box() {
    // Pass-through holes in box
    post_positions = [
        [screw_post_inset, screw_post_inset],
        [external_width - screw_post_inset, screw_post_inset],
        [screw_post_inset, external_depth - screw_post_inset],
        [external_width - screw_post_inset, external_depth - screw_post_inset]
    ];

    for (pos = post_positions) {
        translate([pos[0], pos[1], -1])
            cylinder(h = base_thickness + 2,
                    d = screw_hole_diameter,
                    $fn = 30);
    }
}

module screw_holes_lid() {
    // Countersunk holes in lid
    post_positions = [
        [screw_post_inset, screw_post_inset],
        [external_width - screw_post_inset, screw_post_inset],
        [screw_post_inset, external_depth - screw_post_inset],
        [external_width - screw_post_inset, external_depth - screw_post_inset]
    ];

    for (pos = post_positions) {
        translate([pos[0], pos[1], -1]) {
            // Through hole
            cylinder(h = top_thickness + lip_height + 2,
                    d = screw_hole_diameter,
                    $fn = 30);
            // Countersink
            cylinder(h = screw_head_depth + 1,
                    d = screw_head_diameter,
                    $fn = 30);
        }
    }
}

// ============================================================================
// UTILITY MODULES
// ============================================================================

module rounded_box(width, depth, height, radius) {
    hull() {
        for (x = [radius, width - radius]) {
            for (y = [radius, depth - radius]) {
                translate([x, y, 0])
                    cylinder(h = height, r = radius, $fn = 30);
            }
        }
    }
}

module rounded_slot(width, length, depth) {
    hull() {
        translate([0, width/2, 0])
            cylinder(h = depth, r = width/2, $fn = 20);
        translate([length - width, width/2, 0])
            cylinder(h = depth, r = width/2, $fn = 20);
    }
}

// ============================================================================
// END OF FILE
// ============================================================================
