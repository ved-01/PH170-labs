from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calculate_field():
    net_field = None  

    if request.method == 'POST':
        charge_type = request.form['charge_type']

        if charge_type == 'P':
            charge_x = float(request.form['charge_x'])
            charge_y = float(request.form['charge_y'])
            charge_z = float(request.form['charge_z'])
            charge = float(request.form['charge'])
            ref_x = float(request.form['ref_x'])
            ref_y = float(request.form['ref_y'])
            ref_z = float(request.form['ref_z'])
            net_field = calculate_point_charge_field(charge_x, charge_y, charge_z, charge, ref_x, ref_y, ref_z)

        elif charge_type == 'L':
            line_charge_x1 = float(request.form['line_charge_x1'])
            line_charge_y1 = float(request.form['line_charge_y1'])
            line_charge_z1 = float(request.form['line_charge_z1'])
            line_charge_x2 = float(request.form['line_charge_x2'])
            line_charge_y2 = float(request.form['line_charge_y2'])
            line_charge_z2 = float(request.form['line_charge_z2'])
            line_charge = float(request.form['line_charge'])
            ref_x = float(request.form['ref_x'])
            ref_y = float(request.form['ref_y'])
            ref_z = float(request.form['ref_z'])
            net_field = calculate_line_charge_field(line_charge_x1, line_charge_y1, line_charge_z1,
                                                    line_charge_x2, line_charge_y2, line_charge_z2,
                                                    line_charge, ref_x, ref_y, ref_z)

        elif charge_type == 'S':
            surface_charge_x = float(request.form['surface_charge_x'])
            surface_charge_y = float(request.form['surface_charge_y'])
            surface_charge_z = float(request.form['surface_charge_z'])
            surface_charge = float(request.form['surface_charge'])
            ref_x = float(request.form['ref_x'])
            ref_y = float(request.form['ref_y'])
            ref_z = float(request.form['ref_z'])
            net_field = calculate_surface_charge_field(surface_charge_x, surface_charge_y, surface_charge_z,
                                                       surface_charge, ref_x, ref_y, ref_z)

    return render_template('index.html', net_field=net_field, css=url_for('static', filename='style.css'))



def calculate_point_charge_field(charge_x, charge_y, charge_z, charge, ref_x, ref_y, ref_z):
    dx = ref_x - charge_x
    dy = ref_y - charge_y
    dz = ref_z - charge_z
    r = (dx**2 + dy**2 + dz**2)**0.5
    e_field = (9e9 * charge) / (r**2)
    ex = e_field * (dx / r)
    ey = e_field * (dy / r)
    ez = e_field * (dz / r)
    return ex, ey, ez


def calculate_line_charge_field(line_charge_x1, line_charge_y1, line_charge_z1,
                                line_charge_x2, line_charge_y2, line_charge_z2, line_charge,
                                ref_x, ref_y, ref_z):
    dx1 = ref_x - line_charge_x1
    dy1 = ref_y - line_charge_y1
    dz1 = ref_z - line_charge_z1
    dx2 = ref_x - line_charge_x2
    dy2 = ref_y - line_charge_y2
    dz2 = ref_z - line_charge_z2
    dl_x = line_charge_x2 - line_charge_x1
    dl_y = line_charge_y2 - line_charge_y1
    dl_z = line_charge_z2 - line_charge_z1
    dl = (dl_x**2 + dl_y**2 + dl_z**2)**0.5
    r1 = (dx1**2 + dy1**2 + dz1**2)**0.5
    r2 = (dx2**2 + dy2**2 + dz2**2)**0.5
    e_field = (9e9 * line_charge * dl) / ((r1 + r2) * (r1 + r2 + dl))
    ex = e_field * ((dx2 / r2) - (dx1 / r1))
    ey = e_field * ((dy2 / r2) - (dy1 / r1))
    ez = e_field * ((dz2 / r2) - (dz1 / r1))
    return ex, ey, ez


def calculate_surface_charge_field(surface_charge_x, surface_charge_y, surface_charge_z,
                                   surface_charge, ref_x, ref_y, ref_z):
    dx = ref_x - surface_charge_x
    dy = ref_y - surface_charge_y
    dz = ref_z - surface_charge_z
    r = (dx**2 + dy**2 + dz**2)**0.5
    e_field = (9e9 * surface_charge * 2) / r
    ex = e_field * (dx / r)
    ey = e_field * (dy / r)
    ez = e_field * (dz / r)
    return ex, ey, ez


if __name__ == '__main__':
    app.run(debug=True)
