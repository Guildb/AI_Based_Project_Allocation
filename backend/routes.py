from flask import request, jsonify, make_response
from flask_cors import CORS
import traceback
from database import *
from app import *
import sys
import logging
import bcrypt

def configure_routes(app):
    logging.basicConfig(level=logging.DEBUG)
    
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

    @app.route('/logout', methods=['POST', 'OPTIONS'])
    @token_required
    def logout(current_user):
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/login', methods=['POST', 'OPTIONS'])
    def login():
        

        logging.info("Login route hit")
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
            time = data.get('time')
            
            logging.info(f"Attempting to log in user: {email}")
            
            if not email or not password:
                return jsonify({'error': 'Please provide email and password'}), 400
            
            credentials  = get_user_credentials(email)
            
            logging.info(f"got user credentials: {credentials}")
            
            if not credentials:
                return jsonify({'error': 'Invalid email or password'}), 401
            
            user_id, password_hash = credentials
            logging.info(f"Found user ID {user_id} for email: {email}")
            password = password.encode('utf-8')
            
            if bcrypt.checkpw(password, password_hash):
                logging.info(f"Password verified for user ID: {user_id}")
                token = create_token(user_id, time )
                return jsonify({'token': token}), 200
                

        except Exception as e:
            # Consider logging the exception here for debugging
            logging.exception("An error occurred during the login process:")
            return jsonify({'error': 'Failed to login'}), 500

    @app.route('/changeUserType', methods=['POST'])
    @token_required
    def change_user_type(current_user):
        data = request.get_json()
        userId = data.get('id')
        newType = data.get('newType')

        if not userId or not newType:
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
    @token_required
    def addArea(current_user):
        logging.info("adding Area")
        logging.info(request.headers)
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
    @token_required
    def addExpertise(current_user):
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
    @token_required
    def change_tutor(current_user):
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

    @app.route('/addProject', methods=['POST', 'OPTIONS'])
    @token_required
    def addProject(current_user):
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()
        
        try:
            data = request.get_json()
            project = data.get('project')
            success, message = add_project(project)

            if success:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 500
        except Exception as e:
            app.logger.error(f"Unexpected error while adding project: {e}", exc_info=True)
            return jsonify({'error': "An unexpected error occurred"}), 500

