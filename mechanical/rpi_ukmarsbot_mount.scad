//
//
//
use<submodules/motor_bracket_standard2.scad>;

// https://blog.prusaprinters.org/parametric-design-in-openscad_8758/
module rounded_plate(x, y, thickness, radius) {
    hull() {
        translate([radius, radius]) cylinder(r = radius, h = thickness, $fn=25);
        translate([x - radius, radius]) cylinder(r = radius, h = thickness, $fn=25);
        translate([x - radius, y - radius]) cylinder(r = radius, h = thickness, $fn=25);
        translate([radius, y - radius]) cylinder(r = radius, h = thickness, $fn=25);
    }
}
module four_posts(x, y, thickness, radius, r2) {
    translate([radius, radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        cylinder(r = r2, h = thickness+0.1, $fn=25);
    }
    translate([x - radius, radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        cylinder(r = r2, h = thickness+0.1, $fn=25);
    }
    translate([x - radius, y - radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        cylinder(r = r2, h = thickness+0.1, $fn=25);
    }
    translate([radius, y - radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        cylinder(r = r2, h = thickness+0.1, $fn=25);
    }
}

module support(x, y, thickness, radius, f=25) {
    translate([x, y])
        cylinder(r = radius, h = thickness, $fn=f);
    
}

pizero_x = 65;
pizero_y = 30;
corner_r = 3;
hole_d = 2.75;
hole_r = hole_d / 2;
plate_height = 3;
cut_off = 0.1;
support_height = plate_height + 4;

// Basic Raspberry Pi support
module basic_pi_zero_support()
{
    difference() {
        rounded_plate(pizero_x, pizero_y, plate_height, 3);
        
        // remove some material - to make it lighter
        // also misses mini-USB socket
        translate([0,0,-0.1]) hull /* union */ () {
            support(pizero_x/4, pizero_y/2, plate_height+0.2, 12, f=50);
            support(pizero_x/4*3, pizero_y/2, plate_height+0.2, 12, f=50);
        }
    }
    four_posts(pizero_x, pizero_y, support_height, 3, hole_r);

    // don't need central support, board is strong enough
    //support(pizero_x/2, pizero_y/2, support_height, 3);
}

// Connection to UK MARS Bot
module connection_to_UKMARSBot(x, y)
{
    //translate([0, -pizero_y-0.1, -1 /*(plate_height-2)*/] ) 
    difference() {
        rounded_plate(x, y, plate_height, 3);
        
        // remove some material - to make it lighter
        // also misses mini-USB socket
        translate([0,-y/2,-0.1]) hull() { // union() {
            support(x/4, y/2, plate_height+0.2, 12, f=50);
            support(x/4*3, y/2, plate_height+0.2, 12, f=50);
        }
    }
}

distance_between_motor_mount_holes = 2.15 * 25.4; // according to ukmarsbot_dimensions.png
plate_y_normal = 28;
plate_top_height = 11+3;
height_above_top_motor_plate = 2;
plate_z_new = 7+1;
plate_motor_mount_overlap = 2.5;


translate([-pizero_x/2, plate_y_normal/2-plate_motor_mount_overlap, plate_top_height+height_above_top_motor_plate])
{
    //color("PaleTurquoise")
    basic_pi_zero_support();
    translate([10,-12,0]) connection_to_UKMARSBot(distance_between_motor_mount_holes-10, 15);
}

//edge_to_motor_hole_offset = (((3.2 - 2.15)/2) - 0.35) * 25.4;

//translate([edge_to_motor_hole_offset, 0, 0])
{
    translate([-distance_between_motor_mount_holes/2, 0, 0]) 
    { 
        make_motor_mount(); // plate_z=plate_z_new);
        difference()
        {
            translate([-4,4,11])
            {
                cube([11.5,10,8]);
    //            cylinder();
            }
            translate([0, 8.9, 0])
            {
                cylinder(20, 3, 3, $fn=40);
            }
        }
    }
    translate([distance_between_motor_mount_holes/2, 0, 0]) 
    {
        rotate([0, 0, 180]) make_motor_mount(); //plate_z=plate_z_new);
        difference()
        {
            translate([-7.5,4,11]) 
            {
                cube([11.5,10,8]);
            }
            translate([0, 8.9, 0])
            {
                cylinder(20, 3, 3, $fn=40);
            }
        }
    }
}


