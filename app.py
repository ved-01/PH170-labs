from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

class Charge:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge

class LineCharge:
    def __init__(self, start, end, charge_density):
        self.start = start
        self.end = end
        self.charge_density = charge_density

class SurfaceCharge:
    def __init__(self, position, charge_density):
        self.position = position
        self.charge_density = charge_density

def calculate_net_field(reference_point, charges, line_charges, surface_charges):
    net_field = np.zeros(3)
    for charge in charges:
        distance = reference_point - charge.position
        field = charge.charge * distance / np.linalg.norm(distance)**2
        net_field += field

    for line_charge in line_charges:
        line_vector = line_charge.end - line_charge.start
        length = np.linalg.norm(line_vector)
        direction = line_vector / length
        field = line_charge.charge_density * direction / (2 * np.pi * length)
        net_field += field

    for surface_charge in surface_charges:
        field = surface_charge.charge_density * np.array([0, 0, 1]) / (2 * surface_charge.position[2])
        net_field += field

    return net_field

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        charge_type = request.form['charge_type']

        charges = []
        line_charges = []
        surface_charges = []

        if charge_type.lower() == 'p':
            num_charges = int(request.form['num_charges'])
            for i in range(num_charges):
                x = float(request.form[f'charge_{i}_x'])
                y = float(request.form[f'charge_{i}_y'])
                z = float(request.form[f'charge_{i}_z'])
                charge = float(request.form[f'charge_{i}'])
                charges.append(Charge(np.array([x, y, z]), charge))

        elif charge_type.lower() == 'l':
            num_line_charges = request.form['num_line_charges']
            if num_line_charges and num_line_charges.strip().isdigit():
                num_line_charges = int(num_line_charges)
                for i in range(num_line_charges):
                    x1 = float(request.form[f'line_charge_{i}_x1'])
                    y1 = float(request.form[f'line_charge_{i}_y1'])
                    z1 = float(request.form[f'line_charge_{i}_z1'])
                    x2 = float(request.form[f'line_charge_{i}_x2'])
                    y2 = float(request.form[f'line_charge_{i}_y2'])
                    z2 = float(request.form[f'line_charge_{i}_z2'])
                    charge_density = float(request.form[f'line_charge_{i}'])
                    line_charges.append(LineCharge(np.array([x1, y1, z1]), np.array([x2, y2, z2]), charge_density))

        elif charge_type.lower() == 's':
            num_surface_charges = int(request.form['num_surface_charges'])
            for i in range(num_surface_charges):
                x = float(request.form[f'surface_charge_{i}_x'])
                y = float(request.form[f'surface_charge_{i}_y'])
                z = float(request.form[f'surface_charge_{i}_z'])
                charge_density = float(request.form[f'surface_charge_{i}'])
                surface_charges.append(SurfaceCharge(np.array([x, y, z]), charge_density))

        ref_x = float(request.form['ref_x'])
        ref_y = float(request.form['ref_y'])
        ref_z = float(request.form['ref_z'])
        reference_point = np.array([ref_x, ref_y, ref_z])

        net_field = calculate_net_field(reference_point, charges, line_charges, surface_charges)
        return render_template('index.html', net_field=net_field)

    return render_template('index.html')
