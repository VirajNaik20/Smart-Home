import abc
import os
import json
from chalice import Blueprint
from chalice import Response
import requests
from chalicelib.miscFunctions import authorize_token

mainService = Blueprint(__name__)
import psycopg2
import jwt

# Authorization function
def authorize_Token(authorization):
    try:
        token = authorization.split(' ')[1]
    except:
        return False
    try:
        decoded = jwt.decode(token, os.environ['mysmartswitch20'], algorithms=['RS256'])
        return decoded
    except:
        return False
    pass


 # Helper function to generate JWT tokens
def generate_tokens(email):
    JWT_SECRET = 'mysmartswitch20'
    payload = {'email': email}
    jwt_token = jwt.encode(payload, JWT_SECRET, algorithm='RS256')
    return jwt_token.decode('utf-8')

class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password


@mainService.route('/', methods=['GET'], cors=True)
def changeEnvironment():
    responseMessage = {}
    responseSubMessage = {}
    try:
        
        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)
        
        if authorizationResponse['errorCode'] == 0:
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
    responseMessage = {}
    responseSubMessage = {}
    try:
        
        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)

        print("hi 1")
        
        if authorizationResponse['errorCode'] == 0:
            email = mainService.current_request.json_body.get('email')
            password = mainService.current_request.json_body.get('password')

            # Validate email and password inputs
            if not email or not password:
                raise ValueError("Email and password are required.")

            # Connect to the database
            connection = psycopg2.connect(
                host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                port=5432,
                database="postgres",
                user="postgres",
                password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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

        else:
            responseSubMessage['errorCode'] = authorizationResponse['errorCode']
            responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
            
    except Exception as e:

        responseSubMessage['errorCode'] = 1006
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})


# User Login
@mainService.route('/login', methods=['POST'], cors=True)
def user_login():
    responseMessage = {}
    responseSubMessage = {}
    try:
        
        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)
            
        print("hi 2")

        if authorizationResponse['errorCode'] == 0:
            print("hi 9")
            # Get the email and password from the request body
            email = mainService.current_request.json_body.get('email')
            userPassword = mainService.current_request.json_body.get('password')

            print("hi 10")

             # Connect to the database
            connection = psycopg2.connect(
                host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                port=5432,
                database="postgres",
                user="postgres",
                password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
            )

            cursor = connection.cursor()

            #cursor.row_factory = psycopg2.extras.DictCursor

            # Execute the SQL query to retrieve the user
            cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
            )
            user = cursor.fetchone()

            # Close the cursor and connection
            cursor.close()

            connection.close()

            print("hi 11")

            if user['password'] == userPassword:  # Assuming password is stored at index 3 in the user tuple
            # Generate and return a JSON Web Token (JWT) upon successful authentication
                jwt_token = generate_tokens(email)
                return Response(body={'token': jwt_token}, status_code=200)
            print("hello")
        else:
            responseSubMessage['errorCode'] = authorizationResponse['errorCode']
            responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
            responseMessage['type'] = 'Invalid credentials'
            responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                
    except Exception as e:

        responseSubMessage['errorCode'] = 1006
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})

# Add Device
@mainService.route('/devices', methods=['POST'], cors=True)
def add_device(): 
    print("hi 7")
    responseMessage = {}
    responseSubMessage = {}
    try:
        print("hi 5")    

        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)
            
        if authorizationResponse['errorCode'] == 0:
            print("hi 6")
            # Get the serial number or scanning data from the request body
            serial_number = mainService.current_request.json_body.get('serial_number')
            scanning_data = mainService.current_request.json_body.get('scanning_data')
            print("hi 3")
             # Connect to the database
            connection = psycopg2.connect(
                host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                port=5432,
                database="postgres",
                user="postgres",
                password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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
            print("hi4")
            # Commit the changes to the database
            connection.commit()

            # Close the connection to the database
            connection.close()

            return Response(body={'message': 'Device added successfully.'}, status_code=200)

        else:
            responseSubMessage['errorCode'] = authorizationResponse['errorCode']
            responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                    
    except Exception as e:

        responseSubMessage['errorCode'] = 1006
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
        
       
@mainService.route('/devices/{device_id}/name', methods=['PUT'], cors=True)
def change_device_name(device_id):
    responseMessage = {}
    responseSubMessage = {}
    try:
            
        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)

            
            
        if authorizationResponse['errorCode'] == 0:
            # Get the device name from the request body
            device_name = mainService.current_request.json_body.get('device_name')

            # Connect to the database
            connection = psycopg2.connect(
                    host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                    port=5432,
                    database="postgres",
                    user="postgres",
                    password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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

        else:
            responseSubMessage['errorCode'] = authorizationResponse['errorCode']
            responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                            
    except Exception as e:

            responseSubMessage['errorCode'] = 1006
            responseSubMessage['errorMessage'] = str(e)
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'}) 
        
            


# Switch Management
@mainService.route('/devices/{device_id}/switches', methods=['POST'], cors=True)
def add_switch(device_id):
        responseMessage = {}
        responseSubMessage = {}
        try:
            headers = mainService.current_request.headers
            authorization = headers['authorization']
            authorizationResponse = authorize_token(authorization)
            
            if authorizationResponse['errorCode'] == 0:
                # Get the switch name and status from the request body
                switch_name = mainService.current_request.json_body.get('switch_name')
                switch_status = mainService.current_request.json_body.get('switch_status')

                # Connect to the database
                connection = psycopg2.connect(
                    host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                    port=5432,
                    database="postgres",
                    user="postgres",
                    password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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

            else:
                responseSubMessage['errorCode'] = authorizationResponse['errorCode']
                responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
                responseMessage['type'] = 'Switch not added successfully'
                responseMessage['message'] = responseSubMessage
                return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                
        except Exception as e:

            responseSubMessage['errorCode'] = 1006
            responseSubMessage['errorMessage'] = str(e)
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
        
           

@mainService.route('/devices/{device_id}/switches/{switch_id}', methods=['POST'], cors=True)
def toggle_switch(device_id, switch_id):
        responseMessage = {}
        responseSubMessage = {}
        try:

            headers = mainService.current_request.headers
            authorization = headers['authorization']
            authorizationResponse = authorize_token(authorization)
            
            if authorizationResponse['errorCode'] == 0:
                    # Connect to the database
                connection = psycopg2.connect(
                    host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                    port=5432,
                    database="postgres",
                    user="postgres",
                    password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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

      
            else:
                responseSubMessage['errorCode'] = authorizationResponse['errorCode']
                responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
                responseMessage['type'] = 'error'
                responseMessage['message'] = responseSubMessage
                return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                
        except Exception as e:

            responseSubMessage['errorCode'] = 1006
            responseSubMessage['errorMessage'] = str(e)
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
        
          

# Home Page
@mainService.route('/home_page', methods=['GET'], cors=True)
def home_page():
        responseMessage = {}
        responseSubMessage = {}
        try:
            
            headers = mainService.current_request.headers
            authorization = headers['authorization']
            authorizationResponse = authorize_token(authorization)
            
            if authorizationResponse['errorCode'] == 0:
                    # Connect to the database
                connection = psycopg2.connect(
                    host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                    port=5432,
                    database="postgres",
                    user="postgres",
                    password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
                )

                cursor = connection.cursor()
                print("hi i")
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
    


            else:
                responseSubMessage['errorCode'] = authorizationResponse['errorCode']
                responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
                responseMessage['type'] = 'error'
                responseMessage['message'] = responseSubMessage
                return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                
        except Exception as e:

            responseSubMessage['errorCode'] = 1006
            responseSubMessage['errorMessage'] = str(e)
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
    
           

@mainService.route('/add-user', methods=['POST'], cors=True)
def add_user():
        responseMessage = {}
        responseSubMessage = {}
        try:
            
            headers = mainService.current_request.headers
            authorization = headers['authorization']
            authorizationResponse = authorize_token(authorization)
            
            if authorizationResponse['errorCode'] == 0:
                email = mainService.current_request.json_body.get('email')
                password = mainService.current_request.json_body.get('password')

                # Connect to the database
                connection = psycopg2.connect(
                    host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                    port=5432,
                    database="postgres",
                    user="postgres",
                    password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
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
        

            else:
                responseSubMessage['errorCode'] = authorizationResponse['errorCode']
                responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
                responseMessage['type'] = 'failed'
                responseMessage['message'] = responseSubMessage
                return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
                
        except Exception as e:

            responseSubMessage['errorCode'] = 1006
            responseSubMessage['errorMessage'] = str(e)
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
        

@mainService.route('/home_devices', methods=['GET'], cors=True)
def home_devices():
    responseMessage = {}
    responseSubMessage = {}
    try:
        # Retrieve the user ID from the authorization header
        headers = mainService.current_request.headers
        authorization = headers['authorization']
        authorizationResponse = authorize_token(authorization)
        
        if authorizationResponse['errorCode'] == 0:
            # Connect to the database
            connection = psycopg2.connect(
                host="database-1.crvgm2oeogth.ap-south-1.rds.amazonaws.com",
                port=5432,
                database="postgres",
                user="postgres",
                password="nd327hf823gbfg2379dfh23dhg3v2dfdi23gd",
            )
    
            cursor = connection.cursor()
    
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
    
            return Response(body={'devices': devices}, status_code=200)
    
        else:
            responseSubMessage['errorCode'] = authorizationResponse['errorCode']
            responseSubMessage['errorMessage'] = authorizationResponse['errorMessage']
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=responseMessage, status_code=401, headers={'Content-Type': 'application/json'})
            
    except Exception as e:
        responseSubMessage['errorCode'] = 1006
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})
      
           