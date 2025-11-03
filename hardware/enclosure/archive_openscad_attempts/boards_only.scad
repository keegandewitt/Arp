// Visualization of Two-Board Stack (no enclosure)
// Shows actual component layout

$fn = 30;

// Board dimensions
board_width = 108;
board_depth = 55;
board_thickness = 1.6;

// Stack heights
board_separation = 8;  // standoff height between boards
feather_standoff = 10; // standoff from TOP board to Feather
feather_height = 8;    // Feather M4 total height
oled_standoff = 10;    // standoff from Feather to OLED
oled_height = 7;       // OLED FeatherWing total height

// Jack dimensions
jack_diameter = 6;
midi_diameter = 15.5;
usb_width = 9.5;
usb_height = 3.8;

// Colors
bottom_board_color = [0.2, 0.3, 0.5, 0.9];  // Dark blue
top_board_color = [0.3, 0.5, 0.3, 0.9];     // Green
feather_color = [0.1, 0.1, 0.1, 0.9];       // Black
oled_color = [0.8, 0.2, 0.2, 0.9];          // Red

// BOTTOM BOARD with jacks
translate([0, 0, 0]) {
    color(bottom_board_color) {
        difference() {
            // Board
            cube([board_width, board_depth, board_thickness]);

            // Jack holes at back edge
            translate([0, board_depth - 0.1, board_thickness/2]) {
                rotate([90, 0, 0]) {
                    // USB-C
                    translate([10, 0, 0])
                        cube([usb_width, usb_height, 5], center=true);
                    // CV OUT
                    translate([22, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // TRIG OUT
                    translate([36, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // CC OUT
                    translate([50, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // MIDI OUT
                    translate([72, 0, 0])
                        cylinder(h=5, d=midi_diameter);
                    // MIDI IN
                    translate([96, 0, 0])
                        cylinder(h=5, d=midi_diameter);
                }
            }
        }
    }

    // MIDI FeatherWing area indication
    color([0.8, 0.6, 0.2, 0.3])
        translate([60, 5, board_thickness])
            cube([45, 45, 3]);

    // Standoffs to TOP board
    for (x = [10, board_width-10]) {
        for (y = [10, board_depth-10]) {
            color([0.7, 0.7, 0.7])
                translate([x, y, board_thickness])
                    cylinder(h=board_separation, d=5);
        }
    }
}

// TOP BOARD with jacks
translate([0, 0, board_thickness + board_separation]) {
    color(top_board_color) {
        difference() {
            // Board
            cube([board_width, board_depth, board_thickness]);

            // Jack holes at back edge (TOP ROW)
            translate([0, board_depth - 0.1, board_thickness/2]) {
                rotate([90, 0, 0]) {
                    // CV IN
                    translate([22, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                    // TRIG IN
                    translate([36, 0, 0])
                        cylinder(h=5, d=jack_diameter);
                }
            }
        }
    }

    // Feather M4 standoffs on TOP board
    for (pos = [[60, 15], [60, 40], [105, 15], [105, 40]]) {
        color([0.7, 0.7, 0.7])
            translate([pos[0], pos[1], board_thickness])
                cylinder(h=feather_standoff, d=4);
    }
}

// FEATHER M4 on TOP board
translate([60, 15, board_thickness + board_separation + board_thickness + feather_standoff]) {
    color(feather_color)
        cube([51, 23, feather_height]);

    // Text label
    color("white")
        translate([25, 11.5, feather_height + 0.1])
            linear_extrude(0.5)
                text("M4", size=5, halign="center", valign="center");
}

// OLED standoffs on Feather
translate([60, 15, board_thickness + board_separation + board_thickness + feather_standoff + feather_height]) {
    for (pos = [[5, 5], [5, 18], [46, 5], [46, 18]]) {
        color([0.7, 0.7, 0.7])
            translate([pos[0], pos[1], 0])
                cylinder(h=oled_standoff, d=3);
    }
}

// OLED FeatherWing on Feather
translate([60, 15, board_thickness + board_separation + board_thickness + feather_standoff + feather_height + oled_standoff]) {
    color(oled_color) {
        difference() {
            cube([51, 23, oled_height]);

            // OLED display cutout representation
            translate([15, 7, oled_height - 0.5])
                cube([30, 14, 1]);
        }
    }

    // Buttons on LEFT
    for (i = [0:2]) {
        color("white")
            translate([8, 8 + i*4.5, oled_height - 0.5])
                cylinder(h=1, d=3);
    }

    // Text label
    color("white")
        translate([25, 11.5, 0.1])
            linear_extrude(0.5)
                text("OLED", size=4, halign="center", valign="center");
}

// Dimension lines and labels
module dimension_line(start, end, offset, label) {
    color("yellow") {
        translate([0, 0, offset]) {
            // Line
            hull() {
                translate(start) sphere(0.5);
                translate(end) sphere(0.5);
            }
            // Label
            translate([(start[0]+end[0])/2, (start[1]+end[1])/2, 5])
                text(label, size=3, halign="center");
        }
    }
}

// Height annotations
dimension_line([115, 27.5, 0], [115, 27.5, board_thickness], 0, "1.6mm");
dimension_line([115, 27.5, board_thickness], [115, 27.5, board_thickness + board_separation], 0, "8mm");
dimension_line([115, 27.5, board_thickness + board_separation], [115, 27.5, board_thickness + board_separation + board_thickness], 0, "1.6mm");
dimension_line([115, 27.5, board_thickness + board_separation + board_thickness], [115, 27.5, board_thickness + board_separation + board_thickness + feather_standoff], 0, "10mm");
dimension_line([115, 27.5, board_thickness + board_separation + board_thickness + feather_standoff], [115, 27.5, board_thickness + board_separation + board_thickness + feather_standoff + feather_height], 0, "8mm");

echo("Total stack height = ", board_thickness + board_separation + board_thickness + feather_standoff + feather_height + oled_standoff + oled_height);
