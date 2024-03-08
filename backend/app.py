from flask import Flask, request, jsonify, make_response 
from database import *
from flask_cors import CORS
import os 
from dotenv import load_dotenv
from routes import configure_routes
import bcrypt
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


load_dotenv()


app = Flask(__name__)


## POOL IS IN THE DATABASE FILE
# Allow CORS for requests from 'http://localhost:8080'
CORS(app)

configure_routes(app)

# Calling the function of the create table to ensure that database is created on startup 
with app.app_context():
    create_table_users_if_not_exists()
    create_table_areas_if_not_exists()
    create_table_expertises_if_not_exists()
    create_table_tutors_if_not_exists()
    create_table_students_if_not_exists()
    create_table_tutor_expertise_if_not_exists()
    create_table_projects_if_not_exists()

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
                        'firstName': row[1],
                        'lastName': row[2],
                        'email': row[3],
                        'password': row[4],
                        'type': row[5]
                    }
                    users.append(user)
                return jsonify(users), 200
    except Exception as e:
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)
        
@app.route('/students', methods=['GET'])
def get_students():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT u.id, u.firstName, u.lastName, u.email, u.type, COALESCE(s.student_number, 'NaN') AS student_number
                    FROM "users" u
                    LEFT JOIN "students" s ON u.id = s.user_id
                    WHERE u.type = 'student'
                """)
                rows = cur.fetchall()
                users = []
                for row in rows:
                    user = {
                        'id': row[0],
                        'firstName': row[1],  
                        'lastName': row[2],   
                        'email': row[3],
                        'type': row[4],
                        'student_number': row[5]  
                    }
                    users.append(user)
                return jsonify(users), 200
    except Exception as e:
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)
 
@app.route('/tutors', methods=['GET'])
def get_tutors():
    try:
        tutors = []
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                # Join users, tutors, and areas to fetch basic tutor info and area name
                cur.execute("""
                    SELECT u.id, t.id, u.firstName, u.lastName, u.email, u.type, COALESCE(t.slots, '0') AS slots, COALESCE(a.id, '0') AS areaId
                    FROM "users" u
                    LEFT JOIN "tutors" t ON u.id = t.user_id
                    LEFT JOIN "areas" a ON t.area_id = a.id
                    WHERE u.type = 'tutor'
                """)
                tutor_rows = cur.fetchall()
                
                # Fetch expertises for each tutor
                for row in tutor_rows:
                    cur.execute("""
                        SELECT *
                        FROM "tutor_expertise" te
                        LEFT JOIN "expertises" e ON te.expertise_id = e.id
                        WHERE te.tutor_id = %s
                    """, (row[1],))
                    expertises_results = cur.fetchall()
                    if expertises_results:
                        expertises = [expertise[0] for expertise in expertises_results]
                    else:
                        expertises = []

                    tutors.append({
                        'id': row[0],
                        'tutor_id': row[1],
                        'firstName': row[2],  
                        'lastName': row[3],   
                        'email': row[4],
                        'type': row[5],
                        'slots': row[6],
                        'areaId': row[7],
                        'expertises': expertises
                        
                    })
                
                return jsonify(tutors), 200
    except Exception as e:
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)

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
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)
 
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
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)

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
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)

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
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)
 
@app.route('/get_student', methods=['POST'])
def get_student():
    data = request.get_json()
    id = data.get('id')

    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students WHERE user_id = %s", (id,))
                rows = cur.fetchall()
                students = []
                for row in rows:
                    student = {
                        'id': row[0],
                        'user_id': row[1],
                        'student_number': row[2],
                    }
                    students.append(student)
                return jsonify(students), 200
    except Exception as e:
        logger.exception(f"Error fetching tutors: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)


if __name__ == '__main__':
     # Initialize the database connection pool
    DBPool.get_instance()
    print('Starting the application')
    app.run(host='0.0.0.0', port=5000, debug=True)
