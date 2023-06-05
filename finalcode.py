from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:viraj@localhost:5432/postgres'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Device model
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Switch model
class Switch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, default=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

# User registration
@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User(username=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='User registered successfully')

# User login
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(username=email).first()
    if user and user.password == password:
        # Generate and return JWT token
        return jsonify(token='your_generated_token')

    return jsonify(message='Invalid credentials'), 401

# Add device
@app.route('/add_device', methods=['POST'])
def add_device():
    serial_number = request.json.get('serial_number')
    name = request.json.get('name')
    user_id = int(request.json.get('user_id'))

    device = Device(serial_number=serial_number, name=name, user_id=user_id)
    db.session.add(device)
    db.session.commit()

    return jsonify(message='Device added successfully')

# Device naming
@app.route('/device/<int:device_id>/name', methods=['PUT'])
def name_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify(message='Device not found'), 404

    name = request.json.get('name')
    device.name = name
    db.session.commit()

    return jsonify(message='Device name updated successfully')

# Switch management
@app.route('/device/<int:device_id>/switch', methods=['POST'])
def add_switch(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify(message='Device not found'), 404

    name = request.json.get('name')
    switch = Switch(name=name, device_id=device_id)
    db.session.add(switch)
    db.session.commit()

    return jsonify(message='Switch added successfully')

@app.route('/switch/<int:switch_id>', methods=['PUT'])
def toggle_switch(switch_id):
    switch = Switch.query.get(switch_id)
    if not switch:
        return jsonify(message='Switch not found'), 404

    switch.status = not switch.status
    db.session.commit()

    return jsonify(message='Switch toggled successfully')

# Home page - User information
@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    return jsonify(username=user.username, email=user.username)

# Home page - Add device
@app.route('/user/<int:user_id>/add_device', methods=['POST'])
def add_user_device(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    serial_number = request.json.get('serial_number')
    name = request.json.get('name')

    device = Device(serial_number=serial_number, name=name, user_id=user_id)
    db.session.add(device)
    db.session.commit()

    return jsonify(message='Device added successfully.')

# Home page - Device list
@app.route('/user/<int:user_id>/devices')
def get_user_devices(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    devices = Device.query.filter_by(user_id=user_id).all()
    device_list = [device.name for device in devices]

    return jsonify(devices=device_list)

# Home page - Switch control
@app.route('/switch/<int:switch_id>/toggle', methods=['PUT'])
def toggle_switch1(switch_id):
    switch = Switch.query.get(switch_id)
    if not switch:
        return jsonify(message='Switch not found'), 404

    switch.status = not switch.status
    db.session.commit()

    return jsonify(message='Switch toggled successfully')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
