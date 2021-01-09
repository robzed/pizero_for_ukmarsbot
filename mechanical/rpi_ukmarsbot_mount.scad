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
module four_posts(x, y, thickness, radius, r2, hole) {
    translate([radius, radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        if(hole) { cylinder(r = r2, h = thickness+0.1, $fn=25); }
    }
    translate([x - radius, radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        if(hole) { cylinder(r = r2, h = thickness+0.1, $fn=25); }
    }
    translate([x - radius, y - radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        if(hole) { cylinder(r = r2, h = thickness+0.1, $fn=25); }
    }
    translate([radius, y - radius]) difference() { 
        cylinder(r = radius, h = thickness, $fn=25);
        if(hole) { cylinder(r = r2, h = thickness+0.1, $fn=25); }
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
support_height_front = plate_height + 4;
support_height_mid = plate_height + 6;      // extra clearance for cables

// Basic Raspberry Pi support
module basic_pi_zero_support(hole, support_height=support_height_front)
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
    four_posts(pizero_x, pizero_y, support_height, 3, hole_r, hole);

}

// Connection to UK MARS Bot
module connection_to_UKMARSBot(x, y, xh)
{
    r = 3;
    translate([-x/2 ,-y+0.1 ,0])
    {
        difference() {
            cube([x, y, plate_height]); //, 3);
            union() {
                hull() {
                    translate([-x/2-xh/2+r, -y/6, -0.1]) support(x, y, plate_height+0.2, r, 50);
                    translate([-x/2+xh/2-r, -y, -0.1]) support(x, y, plate_height+0.2, r, 50);
                    translate([-x/2+xh/2-r, -y/6, -0.1]) support(x, y, plate_height+0.2, r, 50);
                    translate([-x/2-xh/2+r, -y, -0.1]) support(x, y, plate_height+0.2, r, 50);
                }
                translate([3, 6.4, -0.1] ) cylinder(r=1.5, h = 30, $fn=25);
                translate([x-3, 6.4, -0.1] ) cylinder(r=1.5, h = 30, $fn=25);
            }
        }
    }
}

module connection_to_UKMARSBot_mid_plate(x, y, xh)
{
    translate([-xh/2, 0, 0]) {
        difference() {            
            translate([-x/2, -y/2, 0]) rounded_plate(x, y, plate_height, 3);
            translate([3, 0, -0.1] ) cylinder(r=1.5, h = 30, $fn=25);
        }
    }
    translate([xh/2, 0, 0]) {
        difference() {
            translate([-x/2, -y/2, 0]) rounded_plate(x, y, plate_height, 3);
            translate([-3, 0, -0.1] ) cylinder(r=1.5, h = 30, $fn=25);
        }
    }
}

distance_between_motor_mount_holes = 2.15 * 25.4; // according to ukmarsbot_dimensions.png
plate_y_normal = 28;
plate_top_height = 11+3;
height_above_top_motor_plate = 2;
plate_motor_mount_overlap = 2.5;



module complete_pi_plate_front(hole=true)
{
    translate([0, plate_y_normal/2-plate_motor_mount_overlap, plate_top_height+height_above_top_motor_plate])
    {
        translate([-pizero_x/2, 0, 0]) basic_pi_zero_support(hole);
        // This is the connection plate
        connection_to_UKMARSBot(distance_between_motor_mount_holes-3.5, 18, distance_between_motor_mount_holes-15.5);
    }
}

module complete_pi_plate_mid(hole=true)
{
    translate([0, 0, plate_top_height+height_above_top_motor_plate])
    {
        translate([-pizero_x/2, plate_y_normal/2-plate_motor_mount_overlap-26, 0]) basic_pi_zero_support(hole, support_height_mid);
        // This is the connection plate
        connection_to_UKMARSBot_mid_plate(12, 10, distance_between_motor_mount_holes-3.5);
    }
}

module motor_mounts(plate_z_new)
{
    // these are the motor mounts
    translate([-distance_between_motor_mount_holes/2, 0, 0]) {
        make_motor_mount(plate_z=plate_z_new);
        //translate([-4,-6,12]) cube([11.5,12,9]);
    }
    
    translate([distance_between_motor_mount_holes/2, 0, 0]) {
        rotate([0, 0, 180]) {
            make_motor_mount(plate_z=plate_z_new);
            //translate([-4,-6,12]) cube([11.5,12,9]);
        }
    }
}


// plate_z_new:
//      5 = touch connecting plate
//      plate_z_new = 7+1;
//      10 = above

// =======================================================
// Different options
//
SELECT_PI_PLATE_FRONT = false;
MOTOR_MOUNTS = true;
SELECT_PI_PLATE_MID = true;
// =======================================================

if(SELECT_PI_PLATE_FRONT)
{
    complete_pi_plate_front();
}
if(MOTOR_MOUNTS)
{
    motor_mounts(5);
}
if(SELECT_PI_PLATE_MID)
{
    complete_pi_plate_mid();
}

