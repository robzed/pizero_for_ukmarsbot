
plate_x_offset = 0;
plate_y_offset = -14;
plate_z_offset = 11;

plate_x_normal = 12;
plate_y_normal = 28;
plate_z_normal = 3;

peg_offset = 4.25;

module pegs(y_offset, x_offset = 0, r=3)
{
    translate([peg_offset+x_offset, y_offset, 3])
    {   
        cylinder(20, r, r, $fn=40);        
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
                pegs(0, 4.7, 1);
            }
        }
    }
}

//make_motor_mount();