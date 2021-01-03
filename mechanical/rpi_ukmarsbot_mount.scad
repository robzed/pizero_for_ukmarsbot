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
support_height = plate_height + 4;

// Basic Raspberry Pi support
module basic_pi_zero_support(hole)
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

distance_between_motor_mount_holes = 2.15 * 25.4; // according to ukmarsbot_dimensions.png
plate_y_normal = 28;
plate_top_height = 11+3;
height_above_top_motor_plate = 2;
plate_motor_mount_overlap = 2.5;



module complete_pi_plate(hole=true)
{
    translate([0, plate_y_normal/2-plate_motor_mount_overlap, plate_top_height+height_above_top_motor_plate])
    {
        translate([-pizero_x/2, 0, 0]) basic_pi_zero_support(hole);
        // This is the connection plate
        connection_to_UKMARSBot(distance_between_motor_mount_holes-3.5, 18, distance_between_motor_mount_holes-15.5);
        //connection_to_UKMARSBot(distance_between_motor_mount_holes+1.55, 25.6);
    }
}

module full_assembly(plate_z_new)
{
    complete_pi_plate();

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

module motor_mounts_only(plate_z_new)
{
    difference()
    {
        union()
        {
            // these are the motor mounts
            translate([-distance_between_motor_mount_holes/2, 0, 0]) {
                make_motor_mount(plate_z=plate_z_new);
            }
            
            translate([distance_between_motor_mount_holes/2, 0, 0]) {
                rotate([0, 0, 180]) { 
                    make_motor_mount(plate_z=plate_z_new);
                }
            }
        }
        union()
        {
            //complete_pi_plate();
            //translate([0.5, 0, 0.5]) complete_pi_plate(hole=false);
            //translate([-0.5, 0, 0.5]) complete_pi_plate(hole=false);
            //translate([0.5, 0, -0.5]) complete_pi_plate(hole=false);
            //translate([-0.5, 0, -0.5]) complete_pi_plate(hole=false);
        }
    }
}
// plate_z_new:
//      5 = touch connecting plate
//      plate_z_new = 7+1;
//      10 = above

// Different options
//

SELECT_FULL_ASSEMBLY = false;
SELECT_COMPLETE_PI_PLATE = true;
MOTOR_MOUNTS_ONLY = false;

if(SELECT_FULL_ASSEMBLY)
{
    full_assembly(5);
}
else if(SELECT_COMPLETE_PI_PLATE)
{
    complete_pi_plate();
}
else if(MOTOR_MOUNTS_ONLY)
{
    motor_mounts_only(5);
}


