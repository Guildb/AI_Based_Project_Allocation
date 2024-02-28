from flask import Flask, request, jsonify, make_response 
import bcrypt
from database import *
from flask_cors import CORS
from flask_mail import Mail
import os 
from dotenv import load_dotenv
from routes import configure_routes


load_dotenv()


app = Flask(__name__)


## POOL IS IN THE DATABASE FILE
# Allow CORS for requests from 'http://localhost:8080'
CORS(app)

configure_routes(app)
@app.route('/message', methods=['GET'])
def get_message():
    return jsonify({'message': 'Hello, World!'})

@app.route('/database', methods=['GET']) ## checking if database is connecting
def get_database():
    return test_db_connection()

# Calling the function of the create table to ensure that database is created on startup 
with app.app_context():
    create_table_users_if_not_exists()
    create_table_areas_if_not_exists()
    create_table_expertises_if_not_exists()
    create_table_tutors_if_not_exists()
    create_table_students_if_not_exists()
    create_table_tutor_expertise_if_not_exists()
    create_table_projects_if_not_exists()
    insert_default_data()

## Code to get all tables apis
@app.route('/users', methods=['GET'])
def get_users():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"users\"")
                rows = cur.fetchall()
                users = []
                for row in rows:
                    user = {
                        'id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'password': row[3],
                        'type': row[4]
                    }
                    users.append(user)
                return jsonify(users), 200
    except Exception as e:
        logger.exception(f"Error fetching users: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
 
@app.route('/areas', methods=['GET'])
def get_areas():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"areas\"")
                rows = cur.fetchall()
                areas = []
                for row in rows:
                    area = {
                        'id': row[0],
                        'name': row[1]
                    }
                    areas.append(area)
                return jsonify(areas), 200
    except Exception as e:
        logger.exception(f"Error fetching areas: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
 
@app.route('/expertises', methods=['GET'])
def get_expertises():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"expertises\"")
                rows = cur.fetchall()
                expertises = []
                for row in rows:
                    expertise = {
                        'id': row[0],
                        'name': row[1],
                        'acronyms': row[2],
                        'area_id': row[3]
                    }
                    expertises.append(expertise)
                return jsonify(expertises), 200
    except Exception as e:
        logger.exception(f"Error fetching expertises: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
 
@app.route('/tutors', methods=['GET'])
def get_tutors():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"tutors\"")
                rows = cur.fetchall()
                tutors = []
                for row in rows:
                    tutor = {
                        'id': row[0],
                        'slots': row[1],
                        'user_id': row[2],
                        'area_id': row[3]
                    }
                    tutors.append(tutor)
                return jsonify(tutors), 200
    except Exception as e:
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/students', methods=['GET'])
def get_students():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"students\"")
                rows = cur.fetchall()
                students = []
                for row in rows:
                    student = {
                        'id': row[0],
                        'user_id': row[1],
                        'student_number': row[2]
                    }
                    students.append(student)
                return jsonify(students), 200
    except Exception as e:
        logger.exception(f"Error fetching students: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/tutor_expertise', methods=['GET'])
def get_tutor_expertise():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"tutor_expertise\"")
                rows = cur.fetchall()
                tutor_expertises = []
                for row in rows:
                    tutor_expertise = {
                        'id': row[0],
                        'tutor_id': row[1],
                        'expertise_id': row[2]
                    }
                    tutor_expertises.append(tutor_expertise)
                return jsonify(tutor_expertises), 200
    except Exception as e:
        logger.exception(f"Error fetching tutor_expertises: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/projects', methods=['GET'])
def get_projects():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"projects\"")
                rows = cur.fetchall()
                projects = []
                for row in rows:
                    project = {
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'student_id': row[3],
                        'tutor_id': row[4],
                        'area_id': row[5],
                        'expertise_id': row[6],
                        'alocated': row[7],
                    }
                    projects.append(project)
                return jsonify(projects), 200
    except Exception as e:
        logger.exception(f"Error fetching projects: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
 
if __name__ == '__main__':
     # Initialize the database connection pool
    DBPool.get_instance()
    print('Starting the application')
    app.run(host='0.0.0.0', port=5000, debug=True)
