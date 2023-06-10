
import os
import json
from chalice import Blueprint
from chalice import Response
mainService = Blueprint(__name__)
import psycopg2
import jwt

@mainService.route('/', methods=['GET'], cors=True)
def processNotifications():

    responseMessage = {}
    responseSubMessage = {}

    try :
        responseMessage['type'] = 'success'
        responseMessage['message'] = 'Hello Viraj'

        return Response(body=responseMessage, status_code=200, headers={'Content-Type': 'application/json'})
    
    except Exception as e:
        responseSubMessage['errorCode'] = 255
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})

# User Registration
@mainService.route('/register', methods=['POST'], cors=True)
def register_user():
    try:
        # Get the email and password from the request body
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')

        # Validate email and password inputs
        if not email or not password:
            raise ValueError("Email and password are required.")

        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Insert the user details into the database
        cursor.execute(
            """
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            """,
            (email, password),
        )

        # Commit the changes to the database
        connection.commit()

        # Close the connection to the database
        connection.close()

        return Response(body={'message': 'User registered successfully.'}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


# User Login
@mainService.route('/login', methods=['POST'], cors=True)
def user_login():
    try:
        # Get the email and password from the request body
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')

        # Verifying the email and password against the stored user details in the database
        user = user.query.filter_by(username=email).first()
        if user and user.password == password:
            # Generate and return a JSON Web Token (JWT) upon successful authentication
            jwt_token = generate_tokens(email)
            return Response(body={'token': jwt_token}, status_code=200)

        return Response(body={'message': 'Invalid credentials'}, status_code=401)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


# Helper function to generate JWT tokens
def generate_tokens(email):
    JWT_SECRET = 'mysmartswitch20'
    payload = {'email': email}
    jwt_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return jwt_token.decode('utf-8')


# Add Device
@mainService.route('/devices', methods=['POST'], cors=True)
def add_device():
    try:
        # Get the serial number or scanning data from the request body
        serial_number = mainService.current_request.json_body.get('serial_number')
        scanning_data = mainService.current_request.json_body.get('scanning_data')

        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Store the device details in the database
        cursor.execute(
            """
            INSERT INTO devices (serial_number, scanning_data)
            VALUES (%s, %s)
            """,
            (serial_number, scanning_data),
        )

        # Commit the changes to the database
        connection.commit()

        # Close the connection to the database
        connection.close()

        return Response(body={'message': 'Device added successfully.'}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


# Device Naming
@mainService.route('/devices/{device_id}/name', methods=['PUT'], cors=True)
def assign_device_name(device_id):
    try:
        # Get the device name from the request body
        device_name = mainService.current_request.json_body.get('device_name')

        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE devices
            SET device_name = %s
            WHERE device_id = %s
            """,
            (device_name, device_id),
        )

        connection.commit()

        connection.close()

        return Response(body={'message': 'Device name assigned successfully.'}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


# Switch Management
@mainService.route('/devices/{device_id}/switches', methods=['POST'], cors=True)
def add_switch(device_id):
    try:
        # Get the switch name and status from the request body
        switch_name = mainService.current_request.json_body.get('switch_name')
        switch_status = mainService.current_request.json_body.get('switch_status')

        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO switches (device_id, switch_name, switch_status)
            VALUES (%s, %s, %s)
            """,
            (device_id, switch_name, switch_status),
        )
        connection.commit()

        connection.close()

        return Response(body={'message': 'Switch added successfully.'}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


@mainService.route('/devices/{device_id}/switches/{switch_id}', methods=['POST'], cors=True)
def toggle_switch(device_id, switch_id):
    try:
        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Fetch the current status of the switch from the database
        cursor.execute(
            """
            SELECT switch_status FROM switches
            WHERE device_id = %s AND switch_id = %s
            """,
            (device_id, switch_id),
        )
        current_status = cursor.fetchone()[0]

        # Toggle the status of the switch
        new_status = 1 - current_status

        # Update the switch status in the database
        cursor.execute(
            """
            UPDATE switches
            SET switch_status = %s
            WHERE device_id = %s AND switch_id = %s
            """,
            (new_status, device_id, switch_id),
        )

        # Commit the transaction
        connection.commit()

        # Close the database connection
        connection.close()
        return Response(body={'message': 'Switch toggled successfully.'}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


# Home Page
@mainService.route('/home_page', methods=['GET'], cors=True)
def home_page():
    try:
        # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        cursor = connection.cursor()

        # Fetch user information (username and email)
        cursor.execute(
            """
            SELECT username, email FROM users
            WHERE user_id = %s
            """,
            ('user_id_here',),
        )
        user_info = cursor.fetchone()

        # Fetch the list of added devices for the user
        cursor.execute(
            """
            SELECT device_name FROM devices
            WHERE user_id = %s
            """,
            ('user_id_here',),
        )
        devices = [device[0] for device in cursor.fetchall()]

        # Close the database connection
        connection.close()

        return Response(body={'user': user_info, 'devices': devices}, status_code=200)

    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)


@mainService.route('/add-user', methods=['POST'], cors=True)
def add_user():
    try:
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')

         # Connect to the database
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="viraj",
        )

        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            """,
            (email, password),
        )
        connection.commit()
        cursor.close()
        connection.close()
        return Response(body={'message': 'User added successfully.'}, status_code=200)
    except Exception as e:
        return Response(body={'error': str(e)}, status_code=400)

