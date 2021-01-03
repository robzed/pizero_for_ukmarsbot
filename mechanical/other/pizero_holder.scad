//
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

module support(x, y, thickness, radius) {
    translate([x, y])
        cylinder(r = radius, h = thickness, $fn=25);
    
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
difference() {
    rounded_plate(pizero_x, pizero_y, plate_height, 3);
    
    // remove some material - to make it lighter
    translate([0,0,-0.1]) union() {
        support(pizero_x/4, pizero_y/2, plate_height+0.2, 12);
        support(pizero_x/4*3, pizero_y/2, plate_height+0.2, 12);
    }
}
four_posts(pizero_x, pizero_y, support_height, 3, hole_r);
support(pizero_x/2, pizero_y/2, support_height, 3);

// Connection to UK MARS Bot
