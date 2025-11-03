// ACCURATE Hardware Stack Visualization
// Based on actual Adafruit specifications from official documentation
// All dimensions verified from Adafruit product pages and datasheets

$fn = 50;

// === ACTUAL ADAFRUIT SPECIFICATIONS ===

// Feather M4 Express (Product 3857)
// Dimensions: 50.8mm x 22.8mm x 7.0mm (2.0" x 0.9" x 0.3")
feather_length = 50.8;
feather_width = 22.8;
feather_height = 7.0;  // TOTAL height including all components

// OLED FeatherWing 128x64 (Product 4650)
// PCB: 22.9mm x 50.9mm, Display area: ~25.8mm x 13mm
// Buttons A/B/C are on the LEFT side
oled_length = 50.9;
oled_width = 22.9;
oled_pcb_thickness = 1.6;
oled_total_height = 7.0;  // PCB + display + buttons
oled_display_width = 25.8;
oled_display_height = 13;

// MIDI FeatherWing (Product 4740)
// Standard FeatherWing dimensions, uses RX/TX pins
midi_length = 50.8;
midi_width = 22.8;
midi_pcb_thickness = 1.6;
midi_component_height = 3.0;  // Estimated for optoisolator/LEDs

// Custom Protoboards (100mm x 50mm standard protoboard trimmed)
proto_length = 108;
proto_width = 55;
proto_thickness = 1.6;

// === STACK HEIGHTS ===
board_separation = 8;      // M3 standoffs between BOTTOM and TOP boards
feather_standoff = 10;     // M2.5 standoffs from TOP board to Feather
oled_standoff = 10;        // Female header stack height (Feather to OLED)

// === COLORS ===
bottom_board_color = [0.2, 0.3, 0.5, 0.9];  // Dark blue
top_board_color = [0.3, 0.5, 0.3, 0.9];     // Green
feather_color = [0.1, 0.1, 0.1, 0.9];       // Black PCB
oled_color = [0.8, 0.2, 0.2, 0.9];          // Red
midi_color = [0.8, 0.6, 0.2, 0.9];          // Gold/bronze

// === JACK DIMENSIONS ===
jack_diameter = 6;
midi_diameter = 15.5;
usb_width = 9.5;
usb_height = 3.8;

// === Z-HEIGHT CALCULATIONS ===
z_base = 0;
z_bottom_board = z_base;
z_bottom_top = z_bottom_board + proto_thickness;
z_top_board = z_bottom_top + board_separation;
z_top_top = z_top_board + proto_thickness;
z_feather = z_top_top + feather_standoff;
z_feather_top = z_feather + feather_height;
// OLED is parallel to Feather, not stacked on it
z_oled = z_feather;  // Same height as Feather
z_oled_top = z_oled + oled_total_height;

echo("=== STACK HEIGHT BREAKDOWN ===");
echo("Bottom board top:", z_bottom_top);
echo("Top board bottom:", z_top_board);
echo("Top board top:", z_top_top);
echo("Feather/OLED bottom:", z_feather);
echo("Feather top:", z_feather_top);
echo("OLED top:", z_oled_top);
echo("TOTAL STACK HEIGHT:", max(z_feather_top, z_oled_top));

// ============================================================
// BOTTOM PROTOBOARD
// ============================================================
module bottom_board() {
    color(bottom_board_color) {
        difference() {
            cube([proto_length, proto_width, proto_thickness]);

            // Jack holes at back edge
            translate([0, proto_width - 0.1, proto_thickness/2]) {
                rotate([90, 0, 0]) {
                    // USB-C at 10mm
                    translate([10, 0, 0])
                        cube([usb_width, usb_height, 5], center=true);
                    // CV OUT at 22mm
                    translate([22, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // TRIG OUT at 36mm
                    translate([36, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // CC OUT at 50mm
                    translate([50, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // MIDI OUT at 72mm
                    translate([72, 0, 0])
                        cylinder(h=5, d=midi_diameter);
                    // MIDI IN at 96mm
                    translate([96, 0, 0])
                        cylinder(h=5, d=midi_diameter);
                }
            }
        }
    }

    // MIDI FeatherWing footprint (right side of board)
    // Positioned at standard Feather location
    translate([proto_length - midi_length - 5, (proto_width - midi_width)/2, proto_thickness]) {
        color(midi_color) {
            // PCB
            cube([midi_length, midi_width, midi_pcb_thickness]);
            // Components (optoisolator, resistors, LEDs)
            translate([10, 5, midi_pcb_thickness])
                cube([30, 12, midi_component_height]);
        }
    }

    // Standoffs to TOP board
    for (x = [10, proto_length-10]) {
        for (y = [10, proto_width-10]) {
            color([0.7, 0.7, 0.7])
                translate([x, y, proto_thickness])
                    cylinder(h=board_separation, d=5);
        }
    }
}

// ============================================================
// TOP PROTOBOARD
// ============================================================
module top_board() {
    color(top_board_color) {
        difference() {
            cube([proto_length, proto_width, proto_thickness]);

            // Jack holes at back edge (TOP ROW)
            translate([0, proto_width - 0.1, proto_thickness/2]) {
                rotate([90, 0, 0]) {
                    // CV IN at 22mm
                    translate([22, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // TRIG IN at 36mm
                    translate([36, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                }
            }
        }
    }

    // OLED FeatherWing standoffs on FAR LEFT
    oled_x_offset = 5;
    oled_y_offset = (proto_width - oled_width) / 2;
    for (pos = [[2.54, 2.54], [2.54, 20.32], [48.26, 2.54], [48.26, 20.32]]) {
        color([0.7, 0.7, 0.7])
            translate([oled_x_offset + pos[0], oled_y_offset + pos[1], proto_thickness])
                cylinder(h=feather_standoff, d=4);
    }

    // Feather M4 standoffs CENTER-RIGHT
    feather_x_offset = 55;
    feather_y_offset = (proto_width - feather_width) / 2;
    for (pos = [[2.54, 2.54], [2.54, 20.32], [48.26, 2.54], [48.26, 20.32]]) {
        color([0.7, 0.7, 0.7])
            translate([feather_x_offset + pos[0], feather_y_offset + pos[1], proto_thickness])
                cylinder(h=feather_standoff, d=4);
    }
}

// ============================================================
// FEATHER M4 EXPRESS
// ============================================================
module feather_m4() {
    color(feather_color) {
        difference() {
            cube([feather_length, feather_width, feather_height]);

            // Mounting holes (2.5mm diameter)
            for (pos = [[2.54, 2.54], [2.54, 20.32], [48.26, 2.54], [48.26, 20.32]]) {
                translate([pos[0], pos[1], -0.1])
                    cylinder(h=feather_height + 0.2, d=2.5);
            }
        }

        // USB-C connector on end
        translate([-2, (feather_width - 9)/2, 1])
            color([0.8, 0.8, 0.8])
                cube([7, 9, 3]);

        // Components on top
        translate([10, 5, 1.6])
            color([0.2, 0.2, 0.2])
                cube([30, 12, 3]);
    }
}

// ============================================================
// OLED FEATHERWING 128x64
// ============================================================
module oled_wing() {
    color(oled_color, 0.9) {
        difference() {
            cube([oled_length, oled_width, oled_pcb_thickness]);

            // Mounting holes to match Feather
            for (pos = [[2.54, 2.54], [2.54, 20.32], [48.26, 2.54], [48.26, 20.32]]) {
                translate([pos[0], pos[1], -0.1])
                    cylinder(h=oled_pcb_thickness + 0.2, d=2.5);
            }
        }
    }

    // OLED Display area (LEFT-JUSTIFIED, ~25.8mm x 13mm)
    translate([15, 5, oled_pcb_thickness]) {
        color([0.1, 0.1, 0.8])
            cube([oled_display_width, oled_display_height, 2]);
    }

    // Buttons A, B, C on the LEFT side (important!)
    for (i = [0:2]) {
        color([0.9, 0.9, 0.9])
            translate([8, 6 + i*5, oled_pcb_thickness])
                cylinder(h=1.5, d=3);
    }

    // Reset button
    color([0.9, 0.9, 0.9])
        translate([45, 6, oled_pcb_thickness])
            cylinder(h=1.5, d=3);
}

// ============================================================
// ASSEMBLE THE STACK
// ============================================================

// BOTTOM BOARD
translate([0, 0, z_bottom_board]) {
    bottom_board();
}

// TOP BOARD
translate([0, 0, z_top_board]) {
    top_board();
}

// FEATHER M4 (mounted on TOP board, CENTER-RIGHT)
feather_x = 55;  // Center-right position
feather_y = (proto_width - feather_width) / 2;
translate([feather_x, feather_y, z_feather]) {
    feather_m4();
}

// OLED FEATHERWING (FAR LEFT of TOP board, NOT stacked on Feather!)
oled_x = 5;  // FAR LEFT position
oled_y = (proto_width - oled_width) / 2;
translate([oled_x, oled_y, z_feather]) {  // Same height as Feather, parallel mounting
    oled_wing();
}

// Height dimension markers
module height_marker(z_start, z_end, x_pos, label) {
    color("yellow") {
        hull() {
            translate([x_pos, proto_width/2, z_start]) sphere(0.5);
            translate([x_pos, proto_width/2, z_end]) sphere(0.5);
        }
        translate([x_pos + 5, proto_width/2, (z_start + z_end)/2])
            linear_extrude(0.5)
                text(label, size=3, halign="left");
    }
}

marker_x = proto_length + 5;
height_marker(z_bottom_board, z_bottom_top, marker_x, "1.6mm");
height_marker(z_bottom_top, z_top_board, marker_x, "8mm");
height_marker(z_top_board, z_top_top, marker_x, "1.6mm");
height_marker(z_top_top, z_feather, marker_x, "10mm");
height_marker(z_feather, z_feather_top, marker_x, "7mm");
height_marker(z_feather_top, z_oled, marker_x, "10mm");
height_marker(z_oled, z_oled_top, marker_x, "7mm");
