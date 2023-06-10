import os
import json
from chalice import Blueprint, Response
from chalicelib.dbConnections import getDbConnection
from chalicelib.mainService import generate_tokens
import psycopg2
import psycopg2.extras
import jwt

mainService = Blueprint(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="viraj",
    )
    return connection

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
    

@mainService.route('/register', methods=['POST'], cors=True)
def register_user():
    try:
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')
        if not email or not password:
            raise ValueError("Email and password are required.")
        
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
        return Response(body={'message': 'User registered successfully.'}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/login', methods=['POST'], cors=True)
def user_login():
    try:
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email = %s
            """,
            (email,),
        )
        user = cursor.fetchone()
        if user and user['password'] == password:
            jwt_token = generate_tokens(email)
            cursor.close()
            connection.close()

            return Response(body={'token': jwt_token}, status_code=200)
        cursor.close()
        connection.close()

        return Response(body={'message': 'Invalid credentials'}, status_code=401)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/devices', methods=['POST'], cors=True)
def add_device():
    try:
        serial_number = mainService.current_request.json_body.get('serial_number')
        scanning_data = mainService.current_request.json_body.get('scanning_data')

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            INSERT INTO devices (serial_number, scanning_data)
            VALUES (%s, %s)
            """,
            (serial_number, scanning_data),
        )
        connection.commit()
        cursor.close()
        connection.close()
        return Response(body={'message': 'Device added successfully.'}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/devices/{device_id}/name', methods=['PUT'], cors=True)
def assign_device_name(device_id):
    try:
        device_name = mainService.current_request.json_body.get('device_name')

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            UPDATE devices
            SET device_name = %s
            WHERE device_id = %s
            """,
            (device_name, device_id),
        )
        connection.commit()
        cursor.close()
        connection.close()

        return Response(body={'message': 'Device name assigned successfully.'}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/devices/{device_id}/switches', methods=['POST'], cors=True)
def add_switch(device_id):
    try:
        switch_name = mainService.current_request.json_body.get('switch_name')
        switch_status = mainService.current_request.json_body.get('switch_status')

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            INSERT INTO switches (device_id, switch_name, switch_status)
            VALUES (%s, %s, %s)
            """,
            (device_id, switch_name, switch_status),
        )
        connection.commit()

        cursor.close()
        connection.close()

        return Response(body={'message': 'Switch added successfully.'}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/devices/{device_id}/switches/{switch_id}', methods=['POST'], cors=True)
def toggle_switch(device_id, switch_id):
    try:
        switch_status = mainService.current_request.json_body.get('switch_status')

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            UPDATE switches
            SET switch_status = %s
            WHERE device_id = %s AND switch_id = %s
            """,
            (switch_status, device_id, switch_id),
        )
        connection.commit()

        cursor.close()

        connection.close()

        return Response(body={'message': 'Switch toggled successfully.'}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/home', methods=['GET'], cors=True)
def home_page():
    try:
        token = mainService.current_request.headers.get('Authorization')
        email = decode_jwt_token(token)

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(
            """
            SELECT * FROM devices
            WHERE email = %s
            """,
            (email,),
        )
        devices = cursor.fetchall()

        cursor.close()

        connection.close()

        return Response(body={'devices': devices}, status_code=200)
    
    except Exception as e:

        return Response(body={'error': str(e)}, status_code=400)

@mainService.route('/add-user', methods=['POST'], cors=True)
def add_user():
    try:
        email = mainService.current_request.json_body.get('email')
        password = mainService.current_request.json_body.get('password')

        connection = get_db_connection()

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

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





