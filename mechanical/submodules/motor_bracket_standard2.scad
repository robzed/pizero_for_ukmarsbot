
plate_x_offset = 0;
plate_y_offset = -14;
plate_z_offset = 11;

plate_x_normal = 12;
plate_y_normal = 28;
plate_z_normal = 3;

peg_offset = 4.25;

// stop up top holes
//translate([2,-11.5,10]) cube([5,23,2]);
module pegs(y_offset)
{
    translate([peg_offset, y_offset, -2])
    {   
//        difference()
        {
            //cylinder(20, 1.5, 1.5, $fn=20);
            translate([0, 0, 5])
            {
                cylinder(20, 3, 3, $fn=40);
            }
        
            // cutout clips
            //translate([-5, -0.5, -0.01]) cube([10, 1, 2]);
        }
    }
}


module make_motor_mount(plate_x = plate_x_normal, plate_y = plate_y_normal, plate_z = plate_z_normal)
{
    translate([-peg_offset, 0, 0])
    {
        import("pololu-gear-motor-bracket-standard.stl");
        difference() 
        {
            translate([plate_x_offset, plate_y_offset, plate_z_offset]) {
                color("white") cube([plate_x,plate_y,plate_z],center=false);
            }
            union()
            {
                pegs(8.9);
                pegs(-8.9);
            }
        }
    }
}

//make_motor_mount();