// Visualization of Two-Board Stack with ACTUAL CAD MODELS
// Uses Adafruit STL files from GitHub CAD Parts repository

$fn = 30;

// Board dimensions
board_width = 108;
board_depth = 55;
board_thickness = 1.6;

// Stack heights
board_separation = 8;  // standoff height between boards
feather_standoff = 10; // standoff from TOP board to Feather
oled_standoff = 10;    // standoff from Feather to OLED

// Jack dimensions
jack_diameter = 6;
midi_diameter = 15.5;
usb_width = 9.5;
usb_height = 3.8;

// Colors
bottom_board_color = [0.2, 0.3, 0.5, 0.9];  // Dark blue
top_board_color = [0.3, 0.5, 0.3, 0.9];     // Green

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

    // ACTUAL MIDI FeatherWing model on BOTTOM board
    color([0.8, 0.6, 0.2])
        translate([60, 5, board_thickness]) {
            // Import actual STL - positioned at right side of board
            import("MIDI_Wing.stl");
        }

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
    for (pos = [[60, 15], [60, 38], [106, 15], [106, 38]]) {
        color([0.7, 0.7, 0.7])
            translate([pos[0], pos[1], board_thickness])
                cylinder(h=feather_standoff, d=4);
    }
}

// ACTUAL FEATHER M4 model on TOP board
translate([60, 15, board_thickness + board_separation + board_thickness + feather_standoff]) {
    // Import actual STL from Adafruit
    import("Feather_M4.stl");

    // OLED standoffs on Feather (female headers - 10mm stacking height)
    for (pos = [[5, 5], [5, 18], [46, 5], [46, 18]]) {
        color([0.7, 0.7, 0.7])
            translate([pos[0], pos[1], 0])
                cylinder(h=oled_standoff, d=3);
    }
}

// ACTUAL OLED FeatherWing model stacked on Feather
translate([60, 15, board_thickness + board_separation + board_thickness + feather_standoff + oled_standoff]) {
    // Import actual STL - note buttons are on LEFT side
    import("OLED_Wing.stl");
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
            // Label as 3D text
            translate([(start[0]+end[0])/2, (start[1]+end[1])/2, 5])
                linear_extrude(0.5)
                    text(label, size=3, halign="center");
        }
    }
}

// Height annotations
dimension_line([115, 27.5, 0], [115, 27.5, board_thickness], 0, "1.6mm");
dimension_line([115, 27.5, board_thickness], [115, 27.5, board_thickness + board_separation], 0, "8mm");
dimension_line([115, 27.5, board_thickness + board_separation], [115, 27.5, board_thickness + board_separation + board_thickness], 0, "1.6mm");
dimension_line([115, 27.5, board_thickness + board_separation + board_thickness], [115, 27.5, board_thickness + board_separation + board_thickness + feather_standoff], 0, "10mm");

echo("STL models imported from Adafruit CAD Parts repository");
echo("Feather M4 Express: 3857, OLED Wing: 4650, MIDI Wing: 4740");
