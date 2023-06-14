from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_field():
    if request.method == 'POST':
        charge_type = request.form['charge_type']
        ref_x = float(request.form['ref_x'])
        ref_y = float(request.form['ref_y'])
        ref_z = float(request.form['ref_z'])
        
        if charge_type == 'P':
            charge_x = float(request.form['charge_x'])
            charge_y = float(request.form['charge_y'])
            charge_z = float(request.form['charge_z'])
            charge = float(request.form['charge'])
            
            # Calculate electric field for point charge
            net_field = calculate_point_charge_field(charge_x, charge_y, charge_z, charge, ref_x, ref_y, ref_z)
            
        elif charge_type == 'L':
            line_charge_x1 = float(request.form['line_charge_x1'])
            line_charge_y1 = float(request.form['line_charge_y1'])
            line_charge_z1 = float(request.form['line_charge_z1'])
            line_charge_x2 = float(request.form['line_charge_x2'])
            line_charge_y2 = float(request.form['line_charge_y2'])
            line_charge_z2 = float(request.form['line_charge_z2'])
            line_charge = float(request.form['line_charge'])
            
            # Calculate electric field for line charge
            net_field = calculate_line_charge_field(line_charge_x1, line_charge_y1, line_charge_z1, line_charge_x2, line_charge_y2, line_charge_z2, line_charge, ref_x, ref_y, ref_z)
            
        elif charge_type == 'S':
            surface_charge_x = float(request.form['surface_charge_x'])
            surface_charge_y = float(request.form['surface_charge_y'])
            surface_charge_z = float(request.form['surface_charge_z'])
            surface_charge = float(request.form['surface_charge'])
            
            # Calculate electric field for surface charge
            net_field = calculate_surface_charge_field(surface_charge_x, surface_charge_y, surface_charge_z, surface_charge, ref_x, ref_y, ref_z)
            
        else:
            net_field = None
            
        return render_template('index.html', net_field=net_field)

    return render_template('index.html', net_field=None)

import math

# Function to calculate the electric field due to a point charge at a reference point
def calculate_point_charge_field(charge_x, charge_y, charge_z, charge, ref_x, ref_y, ref_z):
    k = 9e9  # Coulomb's constant
    dx = ref_x - charge_x
    dy = ref_y - charge_y
    dz = ref_z - charge_z
    r = math.sqrt(dx**2 + dy**2 + dz**2)  # distance between the reference point and charge

    # Calculate electric field components (Ex, Ey, Ez) using Coulomb's law
    Ex = k * charge * dx / r**3
    Ey = k * charge * dy / r**3
    Ez = k * charge * dz / r**3

    return (Ex, Ey, Ez)


# Function to calculate the electric field due to a line charge at a reference point
def calculate_line_charge_field(charge_x1, charge_y1, charge_z1, charge_x2, charge_y2, charge_z2, charge_density, ref_x, ref_y, ref_z):
    k = 9e9  # Coulomb's constant

    # Calculate the vector components of the line segment
    dx = charge_x2 - charge_x1
    dy = charge_y2 - charge_y1
    dz = charge_z2 - charge_z1

    # Calculate the length of the line segment
    dl = math.sqrt(dx**2 + dy**2 + dz**2)

    # Calculate the unit vector in the direction of the line segment
    ux = dx / dl
    uy = dy / dl
    uz = dz / dl

    # Calculate the distance between the reference point and the line segment
    drx = ref_x - charge_x1
    dry = ref_y - charge_y1
    drz = ref_z - charge_z1

    # Calculate the projection of the distance vector onto the line segment
    dr_dot_u = drx * ux + dry * uy + drz * uz

    # Calculate the electric field component due to the line charge
    E = k * charge_density * dl / (4 * math.pi)

    # Calculate the electric field components (Ex, Ey, Ez)
    Ex = E * dr_dot_u * ux / (dr_dot_u**2 + dl**2)
    Ey = E * dr_dot_u * uy / (dr_dot_u**2 + dl**2)
    Ez = E * dr_dot_u * uz / (dr_dot_u**2 + dl**2)

    return (Ex, Ey, Ez)


# Function to calculate the electric field due to a surface charge at a reference point
def calculate_surface_charge_field(charge_density, ref_x, ref_y, ref_z):
    k = 9e9  # Coulomb's constant

    # Calculate the electric field components (Ex, Ey, Ez)
    Ex = 0.0  # Surface charge does not contribute to the electric field
    Ey = 0.0  # Surface charge does not contribute to the electric field
    Ez = k * charge_density / 2

    return (Ex, Ey, Ez)


if __name__ == '__main__':
    app.run(debug=True)
