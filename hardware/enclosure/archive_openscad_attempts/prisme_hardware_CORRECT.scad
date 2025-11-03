// PRISME HARDWARE STACK - EXACT PHYSICAL BUILD
// Based on CORRECT_STACK_LAYOUT.md and PROTOBOARD_LAYOUT.md
// Every component placed EXACTLY as it will be in the final build

$fn = 50;

// ═══════════════════════════════════════════════════════════════
// EXACT DIMENSIONS FROM DOCUMENTATION
// ═══════════════════════════════════════════════════════════════

// Protoboards (custom cut ElectroCookie)
proto_length = 108;
proto_width = 55;
proto_thickness = 1.6;

// Feather M4 Express (Adafruit specs)
feather_length = 50.8;
feather_width = 22.8;
feather_height = 8.0;  // Total with all components

// OLED FeatherWing 128x64 (Adafruit #4650)
oled_length = 50.9;
oled_width = 22.9;
oled_total_height = 7.0;  // PCB + display + buttons

// MCP4728 Quad DAC
mcp4728_length = 20;
mcp4728_width = 20;
mcp4728_height = 10;

// 1200mAh LiPo Battery (Adafruit #258)
battery_length = 50;
battery_width = 35;
battery_height = 8;

// Teyleten Boost Module
boost_length = 17;
boost_width = 10;
boost_height = 4;

// ═══════════════════════════════════════════════════════════════
// Z-HEIGHT STACK (EXACT per CORRECT_STACK_LAYOUT.md)
// ═══════════════════════════════════════════════════════════════

z_base = 4.0;  // Enclosure base clearance
z_bottom_board = z_base;
z_bottom_top = z_bottom_board + proto_thickness;  // 5.6mm

z_board_gap = 8.0;  // M3 standoffs between boards
z_top_board = z_bottom_top + z_board_gap;  // 13.6mm
z_top_top = z_top_board + proto_thickness;  // 15.2mm

z_feather_standoffs = 10.0;  // M2.5 standoffs from TOP board to Feather
z_feather = z_top_top + z_feather_standoffs;  // 25.2mm
z_feather_top = z_feather + feather_height;  // 33.2mm

z_oled_headers = 10.0;  // Female headers STACK OLED ON TOP of Feather
z_oled = z_feather_top + z_oled_headers;  // 43.2mm
z_oled_top = z_oled + oled_total_height;  // 50.2mm

echo("╔═══════════════════════════════════════════════════════╗");
echo("║        PRISME HARDWARE STACK - HEIGHT BREAKDOWN      ║");
echo("╠═══════════════════════════════════════════════════════╣");
echo("  Base clearance:          ", z_base, " mm");
echo("  BOTTOM board (5.6mm):    ", z_bottom_board, " to ", z_bottom_top);
echo("  Board gap (8mm):         ", z_bottom_top, " to ", z_top_board);
echo("  TOP board (15.2mm):      ", z_top_board, " to ", z_top_top);
echo("  Feather standoffs (10mm):", z_top_top, " to ", z_feather);
echo("  Feather M4 (33.2mm):     ", z_feather, " to ", z_feather_top);
echo("  OLED headers (10mm):     ", z_feather_top, " to ", z_oled);
echo("  OLED Wing (50.2mm):      ", z_oled, " to ", z_oled_top);
echo("╠═══════════════════════════════════════════════════════╣");
echo("║  TOTAL INTERNAL HEIGHT: ", z_oled_top, " mm (+ 2mm clearance)  ║");
echo("╚═══════════════════════════════════════════════════════╝");

// ═══════════════════════════════════════════════════════════════
// COMPONENT POSITIONS (from PROTOBOARD_LAYOUT.md)
// ═══════════════════════════════════════════════════════════════

// BOTTOM BOARD jack positions (from left edge)
usb_c_pos = 10;
cv_out_pos = 22;
trig_out_pos = 36;
cc_out_pos = 50;
midi_out_pos = 72;
midi_in_pos = 96;

// LED offsets from jacks
led_offset_35mm = 7;   // For 3.5mm jacks
led_offset_midi = 12;  // For MIDI jacks (CRITICAL!)

// TOP BOARD jack positions
cv_in_pos = 22;
trig_in_pos = 36;

// Feather M4 position on TOP board (center-right, clears CV/TRIG IN)
feather_x_on_top = 57;  // ~60mm from left
feather_y_on_top = (proto_width - feather_width) / 2;

// MCP4728 position on BOTTOM board (center)
mcp4728_x = (proto_length / 2) - (mcp4728_length / 2);
mcp4728_y = (proto_width / 2) - (mcp4728_width / 2);

// Battery UNDER BOTTOM board
battery_x = 29;
battery_y = 10;
battery_z = z_bottom_board - battery_height - 2;  // 2mm clearance below

// Boost module on BOTTOM board (front left)
boost_x = 10;
boost_y = 15;

// ═══════════════════════════════════════════════════════════════
// MODULES - IMPORT REAL CAD FILES
// ═══════════════════════════════════════════════════════════════

module feather_m4_real() {
    import("Feather_M4.stl", convexity=10);
}

module oled_wing_real() {
    import("OLED_Wing.stl", convexity=10);
}

module midi_wing_real() {
    import("MIDI_Wing.stl", convexity=10);
}

// ═══════════════════════════════════════════════════════════════
// COMPONENT MODELS
// ═══════════════════════════════════════════════════════════════

module mcp4728_dac() {
    color([0.2, 0.6, 0.2]) {  // Green module
        cube([mcp4728_length, mcp4728_width, 1.6]);  // PCB
        // Large IC chip
        translate([5, 5, 1.6])
            color([0.1, 0.1, 0.1])
                cube([10, 10, 1.5]);
        // Pin headers
        for (i = [0:3]) {
            translate([2, 2 + i*4, 1.6])
                color([0.8, 0.8, 0.8])
                    cube([1, 2, 6]);
        }
    }
}

module lipo_battery_1200mah() {
    color([0.2, 0.3, 0.6, 0.9]) {
        // Soft pouch with rounded corners
        hull() {
            for (x = [2, battery_length-2])
                for (y = [2, battery_width-2])
                    for (z = [2, battery_height-2])
                        translate([x, y, z])
                            sphere(r=2, $fn=20);
        }
    }
    // JST connector
    color([0.9, 0.9, 0.9])
        translate([battery_length-5, battery_width/2-3, battery_height])
            cube([5, 6, 2]);
}

module teyleten_boost() {
    // Black PCB
    color([0.1, 0.1, 0.1])
        cube([boost_length, boost_width, 1.6]);
    // Large inductor (visible feature)
    color([0.3, 0.3, 0.3])
        translate([boost_length/2-2, boost_width/2-2, 1.6])
            cylinder(h=2.5, d=4, $fn=20);
    // Small SMD components
    color([0.2, 0.2, 0.2]) {
        translate([2, 2, 1.6]) cube([1.5, 1, 0.8]);
        translate([boost_length-3.5, boost_width-3, 1.6]) cube([1.5, 1, 0.8]);
    }
}

module led_3mm(rgb=false) {
    // 3mm LED - exact specs from your documentation
    // Lens: 3mm, Height: 5.4mm, Leads: 27/28.5mm, 3V-3.2V @ 20mA
    color(rgb ? [0.9, 0.4, 0.4, 0.8] : [0.95, 0.95, 0.95, 0.8]) {
        cylinder(h=5.4, d=3, $fn=20);
    }
}

module standoff_m3(height) {
    color([0.7, 0.7, 0.7])
        cylinder(h=height, d=5, $fn=6);
}

module standoff_m25(height) {
    color([0.7, 0.7, 0.7])
        cylinder(h=height, d=4, $fn=6);
}

// ═══════════════════════════════════════════════════════════════
// BOTTOM PROTOBOARD (OUTPUT BOARD)
// ═══════════════════════════════════════════════════════════════

module bottom_board_assembly() {
    translate([0, 0, z_bottom_board]) {
        // Protoboard PCB
        color([0.2, 0.4, 0.6, 0.95]) {
            difference() {
                cube([proto_length, proto_width, proto_thickness]);
                // Jack holes at rear edge
                translate([0, proto_width, proto_thickness/2]) rotate([90, 0, 0]) {
                    translate([usb_c_pos, 0, 0]) cube([9.5, 3.8, 5], center=true);
                    translate([cv_out_pos, 0, 0]) cylinder(h=5, d=6);
                    translate([trig_out_pos, 0, 0]) cylinder(h=5, d=6);
                    translate([cc_out_pos, 0, 0]) cylinder(h=5, d=6);
                    translate([midi_out_pos, 0, 0]) cylinder(h=5, d=15.5);
                    translate([midi_in_pos, 0, 0]) cylinder(h=5, d=15.5);
                }
            }
        }

        // MCP4728 DAC (center of board)
        translate([mcp4728_x, mcp4728_y, proto_thickness])
            mcp4728_dac();

        // Teyleten Boost Module (front left)
        translate([boost_x, boost_y, proto_thickness])
            teyleten_boost();

        // MIDI FeatherWing (right side) - REAL CAD MODEL
        translate([proto_length - feather_length - 5, (proto_width - feather_width)/2, proto_thickness])
            rotate([0, 0, 0])
                midi_wing_real();

        // Activity LEDs at rear edge
        translate([cv_out_pos + led_offset_35mm, proto_width - 0.5, proto_thickness])
            led_3mm(false);  // CV OUT white LED
        translate([trig_out_pos + led_offset_35mm, proto_width - 0.5, proto_thickness])
            led_3mm(true);   // TRIG OUT RGB LED
        translate([cc_out_pos + led_offset_35mm, proto_width - 0.5, proto_thickness])
            led_3mm(false);  // CC OUT white LED
        translate([midi_out_pos + led_offset_midi, proto_width - 0.5, proto_thickness])
            led_3mm(false);  // MIDI OUT white LED
        translate([midi_in_pos + led_offset_midi, proto_width - 0.5, proto_thickness])
            led_3mm(false);  // MIDI IN white LED

        // M3 Standoffs to TOP board (4 corners)
        for (x = [10, proto_length-10])
            for (y = [10, proto_width-10])
                translate([x, y, proto_thickness])
                    standoff_m3(z_board_gap);
    }
}

// ═══════════════════════════════════════════════════════════════
// TOP PROTOBOARD (INPUT BOARD)
// ═══════════════════════════════════════════════════════════════

module top_board_assembly() {
    translate([0, 0, z_top_board]) {
        // Protoboard PCB
        color([0.3, 0.6, 0.3, 0.95]) {
            difference() {
                cube([proto_length, proto_width, proto_thickness]);
                // Jack holes at rear edge (TOP ROW)
                translate([0, proto_width, proto_thickness/2]) rotate([90, 0, 0]) {
                    translate([cv_in_pos, 0, 0]) cylinder(h=5, d=6);
                    translate([trig_in_pos, 0, 0]) cylinder(h=5, d=6);
                }
            }
        }

        // Activity LEDs at rear edge
        translate([cv_in_pos + led_offset_35mm, proto_width - 0.5, proto_thickness])
            led_3mm(false);  // CV IN white LED
        translate([trig_in_pos + led_offset_35mm, proto_width - 0.5, proto_thickness])
            led_3mm(true);   // TRIG IN RGB LED

        // M2.5 Standoffs for Feather M4 (center-right position)
        for (pos = [[2.54, 2.54], [2.54, 20.32], [48.26, 2.54], [48.26, 20.32]])
            translate([feather_x_on_top + pos[0], feather_y_on_top + pos[1], proto_thickness])
                standoff_m25(z_feather_standoffs);
    }
}

// ═══════════════════════════════════════════════════════════════
// FEATHER M4 EXPRESS (on TOP board)
// ═══════════════════════════════════════════════════════════════

module feather_m4_assembly() {
    translate([feather_x_on_top, feather_y_on_top, z_feather]) {
        feather_m4_real();
    }
}

// ═══════════════════════════════════════════════════════════════
// OLED FEATHERWING (STACKED ON TOP of Feather M4)
// ═══════════════════════════════════════════════════════════════

module oled_wing_assembly() {
    translate([feather_x_on_top, feather_y_on_top, z_oled]) {
        oled_wing_real();
    }
}

// ═══════════════════════════════════════════════════════════════
// BATTERY (UNDER BOTTOM BOARD)
// ═══════════════════════════════════════════════════════════════

module battery_assembly() {
    translate([battery_x, battery_y, battery_z])
        lipo_battery_1200mah();
}

// ═══════════════════════════════════════════════════════════════
// ASSEMBLE COMPLETE HARDWARE STACK
// ═══════════════════════════════════════════════════════════════

battery_assembly();
bottom_board_assembly();
top_board_assembly();
feather_m4_assembly();
oled_wing_assembly();

// Height reference markers
color("yellow") {
    translate([proto_length + 10, proto_width/2, 0]) {
        cylinder(h=z_oled_top, d=1);
        translate([0, 0, z_bottom_board]) cube([5, 1, 0.5]);
        translate([0, 0, z_top_board]) cube([5, 1, 0.5]);
        translate([0, 0, z_feather]) cube([5, 1, 0.5]);
        translate([0, 0, z_oled]) cube([5, 1, 0.5]);
        translate([0, 0, z_oled_top]) cube([5, 1, 0.5]);
    }
}
