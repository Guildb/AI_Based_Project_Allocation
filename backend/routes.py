from flask import request, jsonify, make_response
from flask_cors import CORS
import traceback
from database import *
import jwt
import bcrypt

def configure_routes(app):
    CORS(app)

    @app.route('/signup', methods=['POST', 'OPTIONS'])
    def signup():
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()
        
        try:
            data = request.get_json()
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            password = data.get('password')

            if not all([firstName, lastName, email, password]):
                return jsonify({'error': 'All fields must be filled'}), 400

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            store_user_result = store_user_in_database(firstName, lastName, email, password, "student")
            
            if store_user_result:
                error_message, status_code = store_user_result
                return jsonify({'error': error_message}), status_code

            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            logger.exception(f"Exception in signup: {e}")
            return jsonify({'error': 'Failed to signup'}), 500

    def _build_cors_preflight_response():
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password').encode('utf-8')  # Ensure password is in bytes


        if not email or not password:
            return jsonify({'error': 'Please provide email and password'}), 400

        try:
            with DBPool.get_instance().getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT password FROM users WHERE email = %s", (email,))
                    user_record = cur.fetchone()

                    if user_record is None:
                        return jsonify({'error': 'User not found'}), 404

                    hashed_password = user_record[0].encode('utf-8')  # Ensure hashed_password is in bytes
                    if (password):
                        return jsonify({'message': 'Login successful'}), 200
                    else:
                        return jsonify({'error': 'Invalid credentials'}), 401
        except psycopg2.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            DBPool.get_instance().putconn(conn)