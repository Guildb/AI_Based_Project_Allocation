from flask import request, jsonify, make_response
from flask_cors import CORS
import traceback
from database import *
import sys
import logging
import bcrypt

def configure_routes(app):
    
    def _build_cors_preflight_response():
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    @app.route('/signup', methods=['POST', 'OPTIONS'])
    def signup():
        if request.method == 'OPTIONS':
            response = make_response(jsonify({'status': 'OK'}), 200)
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
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
            hashed_password = hashed_password.decode('utf8')
            store_user_result = store_user_in_database(firstName, lastName, email, hashed_password, 'student')
            
            if store_user_result:
                error_message, status_code = store_user_result
                return jsonify({'error': error_message}), status_code

            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            logger.exception(f"Exception in signup: {e}")
            return jsonify({'error': 'Failed to signup'}), 500

    @app.route('/login', methods=['POST', 'OPTIONS'])
    def login():
        logging.basicConfig(level=logging.DEBUG)

        print("Received login request", file=sys.stderr)
        if request.method == 'OPTIONS':
            response = make_response(jsonify({'status': 'OK'}), 200)
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return _build_cors_preflight_response()
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return jsonify({'error': 'Please provide email and password'}), 400

            password_hash = verify_password(email, password)
            password = password.encode('utf-8')
            print(f"Received login request for user: {password}", file=sys.stderr)

            if password_hash and bcrypt.checkpw(password, password_hash):
                return jsonify({'Success': 'Logged in'}), 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401

        except Exception as e:
            # Consider logging the exception here for debugging
            return jsonify({'error': 'Failed to login'}), 500

    @app.route('/changeUserType', methods=['POST'])
    def change_user_type():
        data = request.get_json()
        userId = data.get('id')
        newType = data.get('newType')

        if userId is None or newType is None:
            return jsonify({'error': "Missing 'id' or 'newType' in request"}), 400

        try:
            success, message = change_user_type_db(userId, newType)

            if success:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 404 if message == "User not found" else 500
        except Exception as e:
            app.logger.error(f"Unexpected error while changing user type: {e}", exc_info=True)
            return jsonify({'error': "An unexpected error occurred"}), 500

    @app.route('/addArea', methods=['POST', 'OPTIONS'])
    def addArea():
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()
        
        try:
            data = request.get_json()
            name = data.get('name')

            if not ([name]):
                return jsonify({'error': 'All fields must be filled'}), 400

            store_area_result = store_areas_in_database(name)
            
            if store_area_result:
                error_message, status_code = store_area_result
                return jsonify({'error': error_message}), status_code

            return jsonify({'message': 'Area created successfully'}), 201
        except Exception as e:
            logger.exception(f"Exception in signup: {e}")
            return jsonify({'error': 'Failed to add Area'}), 500

    @app.route('/addExpertise', methods=['POST', 'OPTIONS'])
    def addExpertise():
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()
        
        try:
            data = request.get_json()
            name = data.get('name')
            acronym = data.get('acronym')
            areaId = data.get('area_id')

            if not all([name, acronym, areaId]):
                return jsonify({'error': 'All fields must be filled'}), 400

            error_message, status_code = store_expertises_in_database(name, acronym, areaId)
            
            if error_message:
                return jsonify({'error': error_message}), status_code

            return jsonify({'message': 'Expertise created successfully'}), 201
        except Exception as e:
            logger.exception(f"Exception in addExpertise: {e}")
            return jsonify({'error': 'Failed to add expertise'}), 500

    @app.route('/changeTutors', methods=['POST', 'OPTIONS'])
    def change_tutor():
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()

        try:
            data = request.get_json()
            user = data.get('user')
            success, message = update_user(user)

            if success:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 404 if message == "User not found" else 500
        except Exception as e:
            app.logger.error(f"Unexpected error while changing user type: {e}", exc_info=True)
            return jsonify({'error': "An unexpected error occurred"}), 500


