// ============================================================================
// PRISME Translation Hub - Parametric Enclosure
// ============================================================================
// 3D-printable enclosure for Feather M4 + OLED + MCP4728 CV/Gate I/O
// Designed for semi-transparent PLA filament (prism effect)
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
// OPTIMIZED for custom-cut 75mm × 50mm protoboards
internal_width = 83;    // X-axis (left-right) - fits 75mm boards + 4mm clearance each side
internal_depth = 58;    // Y-axis (front-back) - fits 50mm boards + 4mm clearance each side
internal_height = 50;   // Z-axis (bottom-top) - component stack height

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

// 1/8" (3.5mm) mono jacks - CV and Gate I/O
jack_hole_diameter = 6.0;       // 1/8" jack hole (6mm for panel mount)
jack_spacing = 10;              // 10mm center-to-center spacing

// 5-pin DIN MIDI panel mount
midi_connector_diameter = 15.5; // 5-pin DIN panel mount hole (15mm + tolerance)
midi_spacing = 20;              // 20mm center-to-center spacing

// USB-C panel mount cutout
usb_width = 9.5;                // USB-C connector width (9mm + tolerance)
usb_height = 3.8;               // USB-C connector height (3.5mm + tolerance)

// === JACK POSITIONS (measured from left edge of back panel) ===
// These EXACTLY match the protoboard rear edge layout:
//
// OUTPUT BOARD (bottom row): CV Out (13mm), V/S-Trig (23mm), Custom CC (33mm), USB-C (58.5mm)
// INPUT BOARD (top row):     CV In (13mm), Gate In (23mm), MIDI In (35.5mm), MIDI Out (55.5mm)
//
// The enclosure has wall_thickness offset, so add that to board positions:

board_offset_x = wall_thickness + 4;  // 4mm board margin from left wall
board_offset_y = base_thickness;       // Boards sit on base

// Translate board positions to enclosure positions:
cv_out_x = board_offset_x + 13;        // 13mm from board left edge
vtrig_x = board_offset_x + 23;         // 23mm from board left edge
cc_x = board_offset_x + 33;            // 33mm from board left edge
usb_c_x = board_offset_x + 58.5;       // 58.5mm from board left edge (right edge aligned with MIDI Out)

cv_in_x = board_offset_x + 13;         // 13mm from board left edge
gate_in_x = board_offset_x + 23;       // 23mm from board left edge
midi_in_x = board_offset_x + 35.5;     // 35.5mm from board left edge
midi_out_x = board_offset_x + 55.5;    // 55.5mm from board left edge

// Y positions (height from base):
output_board_jack_y = 15;              // OUTPUT board jacks height (BOTTOM ROW)
input_board_jack_y = 27;               // INPUT board jacks height (TOP ROW)

// === TOP PANEL - OLED AND BUTTONS ===
// OLED cutout (128x64 SH1107 display)
oled_width = 30;                // Display visible area width
oled_height = 16;               // Display visible area height
oled_offset_x = 10;             // From left edge (OPTIMIZED for compact enclosure)
oled_offset_y = 20;             // From front edge (OPTIMIZED for compact enclosure)

// Button holes (OLED FeatherWing: A, B, C)
button_diameter = 6.5;          // 6mm tactile button + tolerance
button_spacing = 11;            // Spacing between button centers
buttons_offset_x = 48;          // From left edge (OPTIMIZED - positioned right of OLED)
buttons_offset_y = 20;          // From front edge (aligned with OLED Y)

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

        // Back panel cutouts (jacks + USB-C + MIDI)
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
// MOUNTING METHOD:
//
// ALL jacks/connectors are soldered directly to protoboard rear edges:
//
// 1/8" (3.5mm) Mono Jacks (5 total):
//   - 3× on OUTPUT board rear edge: CV Out, V-Trig/S-Trig, Custom CC
//   - 2× on INPUT board rear edge: CV In, Gate In
//   - 6mm clearance holes in enclosure
//   - Jacks soldered to board, barrels pass through enclosure holes
//   - No external mounting hardware needed
//
// 5-pin DIN MIDI Jacks (2 total):
//   - 2× on INPUT board rear edge: MIDI In, MIDI Out
//   - Panel-mount DIN jacks
//   - Wired from MIDI FeatherWing TX/RX pins to jack pins
//   - 15.5mm clearance holes in enclosure
//   - Threaded bushing secures from outside
//
// USB-C Panel Mount:
//   - 1× on INPUT board rear edge (positioned at BOTTOM ROW height)
//   - USB-C extension cable from Feather M4 to panel-mount breakout
//   - Connector passes through 9.5mm × 3.8mm rectangular cutout at bottom row
//   - No mounting screws needed
//
// Protoboard Alignment:
//   - Metal standoffs between OUTPUT and INPUT boards
//   - Standoffs ensure perfect jack alignment
//   - Boards mechanically support all connectors
//
// ============================================================================

module back_panel_cutouts() {
    // Rotate 90° and position at back
    // Cutout positions EXACTLY match protoboard rear edge layout
    rotate([90, 0, 0])
    translate([0, 0, -1]) {

        // ===OUTPUT BOARD JACKS (Bottom row)===
        // CV Out (13mm from board left edge)
        translate([cv_out_x, output_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // V-Trig/S-Trig Out (23mm from board left edge)
        translate([vtrig_x, output_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // Custom CC Out (33mm from board left edge)
        translate([cc_x, output_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // === INPUT BOARD JACKS (Top row) ===
        // CV In (13mm from board left edge)
        translate([cv_in_x, input_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // Gate In (23mm from board left edge)
        translate([gate_in_x, input_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = jack_hole_diameter, $fn = 30);

        // MIDI In (35.5mm from board left edge)
        translate([midi_in_x, input_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = midi_connector_diameter, $fn = 40);

        // MIDI Out (55.5mm from board left edge)
        translate([midi_out_x, input_board_jack_y, 0])
            cylinder(h = wall_thickness + 2, d = midi_connector_diameter, $fn = 40);

        // USB-C (67mm from board left edge, BOTTOM ROW - same height as OUTPUT board jacks)
        translate([usb_c_x - (usb_width / 2),
                   output_board_jack_y - (usb_height / 2),
                   0])
            cube([usb_width, usb_height, wall_thickness + 2]);
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
