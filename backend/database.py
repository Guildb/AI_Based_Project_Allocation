import psycopg2
from psycopg2 import pool
import jwt
from functools import wraps
import datetime
import logging
import os
import sys
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv 
from flask import request, jsonify, make_response
import json




logger = logging.getLogger(__name__) 
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SESSION_KEY = os.getenv("SESSION_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
# DATABASE_URL = os.getenv("DATABASE_URL")

class DBPool:
    _instance = None

    @staticmethod
    def get_instance():
        if DBPool._instance is None:
            DBPool._instance = pool.ThreadedConnectionPool(minconn=1, maxconn=20,

                                                           user=DB_USER,
                                                           password=DB_PASSWORD,
                                                           host=DB_HOST,
                                                           port=DB_PORT,
                                                           database=DB_NAME)
        return DBPool._instance

def _build_cors_preflight_response():
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

#functions to create tables
def create_table_users_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "users" (
                            id SERIAL PRIMARY KEY,
                            firstName VARCHAR(255) NOT NULL,
                            lastName VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL UNIQUE,
                            password VARCHAR(255) NOT NULL,
                            type VARCHAR(255) NOT NULL
                        )
                    """)
                    conn.commit()
                    return "Table 'users' created successfully."
                else:
                    return "Table 'users' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_areas_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'areas')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "areas" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL UNIQUE
                        )
                    """)
                    conn.commit()
                    return "Table 'areas' created successfully."
                else:
                    return "Table 'areas' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_expertises_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'expertises')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "expertises" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            acronym VARCHAR(255) NOT NULL,
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """)
                    conn.commit()
                    return "Table 'expertises' created successfully."
                else:
                    return "Table 'expertises' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_tutors_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tutors')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "tutors" (
                            id SERIAL PRIMARY KEY,
                            slots INTEGER NOT NULL,
                            user_id INTEGER REFERENCES "users" (id),
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """)
                    conn.commit()
                    return "Table 'tutors' created successfully."
                else:
                    return "Table 'tutors' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_students_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'students')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "students" (
                            id SERIAL PRIMARY KEY,
                            student_number VARCHAR(255) NOT NULL,
                            user_id INTEGER REFERENCES "users" (id),
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """)
                    conn.commit()
                    return "Table 'students' created successfully."
                else:
                    return "Table 'students' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_tutor_expertise_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tutor_expertise')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "tutor_expertise" (
                            id SERIAL PRIMARY KEY,
                            tutor_id INTEGER REFERENCES "tutors" (id),
                            expertise_id INTEGER REFERENCES "expertises" (id)
                        )
                    """)
                    conn.commit()
                    return "Table 'tutor_expertise' created successfully."
                else:
                    return "Table 'tutor_expertise' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)
            
def create_table_project_expertise_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'project_expertise')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "project_expertise" (
                            id SERIAL PRIMARY KEY,
                            project_id INTEGER REFERENCES "projects" (id),
                            expertise_id INTEGER REFERENCES "expertises" (id)
                        )
                    """)
                    conn.commit()
                    return "Table 'project_expertise' created successfully."
                else:
                    return "Table 'project_expertise' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def create_table_projects_if_not_exists():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'projects')")
                table_exists = cur.fetchone()[0]
                if not table_exists:
                    cur.execute("""
                        CREATE TABLE "projects" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            description VARCHAR(255) NOT NULL,
                            student_id INTEGER REFERENCES "students" (id),
                            tutor_id INTEGER REFERENCES "tutors" (id),
                            area_id INTEGER REFERENCES "areas" (id),
                            alocated BOOLEAN NOT NULL DEFAULT FALSE
                        )
                    """)
                    conn.commit()
                    return "Table 'projects' created successfully."
                else:
                    return "Table 'projects' already exists."
    except psycopg2.Error as e:
        return f"Unable to create table: {e}"
    finally:
            DBPool.get_instance().putconn(conn)


#functions to store data in database
def store_user_in_database(firstName, lastName, email, hashed_password, typeIn):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "users" (firstName, lastName, email, password, type)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (firstName, lastName, email, hashed_password, typeIn))
                    conn.commit()
                    return None  
                except psycopg2.errors.UniqueViolation as e:
                    return "Email address already exists.", 409
                except psycopg2.Error as e:
                    conn.rollback()  
                    return "Failed to insert user.", 500
                except Exception as e:
                    conn.rollback()  
                    return "Unexpected error.", 500
    except psycopg2.Error as e:
        return f"Unable to add user: {e}", 500
    finally:
        DBPool.get_instance().putconn(conn)

def store_areas_in_database(nameIn):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "areas" (name)
                        VALUES (%s)
                    """, (nameIn,))
                    conn.commit()
                    print("Area stored successfully")
                    return "Area stored successfully.", 200
                except psycopg2.errors.UniqueViolation as e:
                    return "Failed to insert area: Area already exists.", 409
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert area:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add area: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_expertises_in_database(name, acronym, area_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "expertises" (name, acronym, area_id)
                        VALUES (%s, %s, %s)
                    """, (name, acronym, area_id))
                    conn.commit()
                    print("Expertise stored successfully")
                    return None, 201
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert expertise:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add expertise: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_tutors_in_database(slots, user_id, area_id):
    try:

        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "tutors" (slots, user_id, area_id)
                        VALUES (%s, %s, %s)
                    """, (slots, user_id, area_id))
                    conn.commit()
                    print("tutor stored successfully")
                    return "tutor stored successfully.", 200
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert tutor:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add tutor: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_students_in_database(student_number, user_id, area_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "students" (student_number, user_id, area_id)
                        VALUES (%s, %s, %s)
                    """, (student_number, user_id, area_id))
                    conn.commit()
                    return "student stored successfully.", 200
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert student:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add student: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_tutor_expertise_in_database(tutor_id, expertise_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "tutor_expertise" (tutor_id, expertise_id)
                        VALUES (%s, %s)
                    """, (tutor_id, expertise_id))
                    conn.commit()
                    print("tutor_expertise stored successfully")
                    return "tutor_expertise stored successfully.", 200
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert tutor_expertise:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_project_expertise_in_database(project_id, expertise_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "project_expertise" (project_id, expertise_id)
                        VALUES (%s, %s)
                    """, (project_id, expertise_id))
                    conn.commit()
                    print("project_expertise stored successfully")
                    return "project_expertise stored successfully.", 200
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert project_expertise:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_projects_in_database(name, description, student_id, tutor_id, area_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                alocated = False
                if student_id and tutor_id:
                    alocated = True
                
                try:
                    cur.execute("""
                        INSERT INTO "projects" (name, description, student_id, tutor_id, area_id, alocated)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """, (name, description, student_id, tutor_id, area_id, alocated))
                    project_id = cur.fetchone()[0]
                    conn.commit()
                    print("project stored successfully")
                    return project_id, 200
                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to insert project:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add project: {e}"
    finally:
            DBPool.get_instance().putconn(conn)
       
#functions to delete data
def delete_student(user):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False
                    cur.execute("""
                                UPDATE "projects"
                                SET student_id = null, alocated = False
                                WHERE student_id = %s;
                                """, (user['student_id'], ))
                    cur.execute("DELETE FROM students WHERE user_id = %s", (user['id'],))
                    cur.execute("DELETE FROM users WHERE id = %s", (user['id'],))
                    conn.commit()
                except psycopg2.Error as e:
                    conn.rollback()  
                    return False, f"Transaction failed: {e}"  
                except Exception as e:
                    conn.rollback() 
                    return False, f"Unexpected error: {e}"
        return True,f"Student deleted successfully"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def delete_tutor(user):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False
                    cur.execute("""
                                UPDATE "projects" 
                                SET tutor_id = null, alocated = False 
                                WHERE tutor_id = %s; 
                                """, (user['tutor_id'], ))
                    cur.execute("DELETE FROM tutor_expertise WHERE tutor_id = %s", (user['tutor_id'],))
                    cur.execute("DELETE FROM tutors WHERE id = %s", (user['tutor_id'],))
                    cur.execute("DELETE FROM users WHERE id = %s", (user['id'],))
                    conn.commit()
                except psycopg2.Error as e:
                    conn.rollback()  
                    return False, f"Transaction failed: {e}"  
                except Exception as e:
                    conn.rollback() 
                    return False, f"Unexpected error: {e}"
        return True, 'Tutor deleted successfully'
    except Exception as e:
        return False, f"Transaction failed: {e}" 

def delete_area(area_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE "projects" SET area_id = null WHERE area_id = %s; """, (area_id, ))
                cur.execute("DELETE FROM areas WHERE id = %s", (area_id,))
                conn.commit()
        return True, 'Area deleted successfully'
    except Exception as e:
        return False, f"Unexpected error: {e}"

def delete_expertise(expertise_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False
                    cur.execute("DELETE FROM tutor_expertise WHERE expertise_id = %s", (expertise_id,))
                    cur.execute("DELETE FROM project_expertise WHERE expertise_id = %s", (expertise_id,))
                    cur.execute("DELETE FROM expertises WHERE id = %s", (expertise_id,))
                    conn.commit()
                except psycopg2.Error as e:
                    conn.rollback()  
                    return False, f"Transaction failed: {e}"
                except Exception as e:
                    conn.rollback() 
                    return False, f"Unexpected error: {e}"
        return True, 'Expertise and related associations deleted successfully'
    except Exception as e:
        return False, f"Unexpected error: {e}"

def delete_project(project_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False
                    cur.execute("DELETE FROM project_expertise WHERE project_id = %s", (project_id,))
                    cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
                    conn.commit()
                except psycopg2.Error as e:
                    conn.rollback()  
                    return False, f"Transaction failed: {e}"  
                except Exception as e:
                    conn.rollback() 
                    return False, f"Unexpected error: {e}"
        return True, 'Tutor deleted successfully'
    except Exception as e:
        return False, f"Unexpected error: {e}"


  

#session functions
def create_token(user_id, time, user_type):
    payload = {
        "user_id": user_id,
        "type": user_type,
        "exp": datetime.utcnow() + timedelta(hours= time) 
    }
    token = jwt.encode(payload, SESSION_KEY, algorithm=ALGORITHM)
    return token

def validate_token(token):
    try:
        payload = jwt.decode(token, SESSION_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None 
    
def token_required(f):
    @wraps(f)  
    def decorated(*args, **kwargs):
        token = None
        if request.method == 'OPTIONS':
            return _build_cors_preflight_response()
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = validate_token(token)
            if data is None:
                raise ValueError('Token is invalid or expired!')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except (jwt.InvalidTokenError, ValueError) as e:
            return jsonify({'message': str(e)}), 401
        
        current_user = data['user_id']
        return f(current_user, *args, **kwargs)

    return decorated

#functions to manipulate the data   
def change_user_type_in_database(cur, userId, newType):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        UPDATE "users"
                        SET type = %s
                        WHERE id = %s;
                    """, (newType, userId))
                    conn.commit()

                    if cur.rowcount == 0:
                        return False, "User not found"
            
                    return True, "User type updated successfully"

                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to change type:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def change_user_type_db(userId,newType):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False 
                    oldType = check_user_type(userId)
                        
                    if newType == "tutor" or newType == "courseLeader":
                        if oldType =="student":
                            delete_old_user(cur, "students", userId )
                            store_tutors_in_database(0, userId, None)
                        change_user_type_in_database(cur, userId, newType)
                        
                        
                    elif newType=="student":
                        if oldType =="tutor" or oldType == "courseLeader":
                            delete_old_user(cur, "tutors", userId )
                        change_user_type_in_database(cur, userId, newType)
                        store_students_in_database(0, userId)

                    conn.commit()  
                    return True, "User updated successfully" 
                except psycopg2.Error as e:
                    conn.rollback()  
                    return False, f"Transaction failed: {e}" 
                except Exception as e:
                    conn.rollback() 
                    return False, f"Unexpected error: {e}"  
    except psycopg2.Error as e:
        return False, f"Unable to create link: {e}"  
    finally:
        DBPool.get_instance().putconn(conn) 

def check_user_type(userId):
    with DBPool.get_instance().getconn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT type FROM "users" WHERE id = %s', (userId,))
            oldType = cur.fetchone()[0]
            return oldType

def update_user(user):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                conn.autocommit = False 
                current_user_data = fetch_current_user_data(cur, user['id'])
                if not current_user_data:
                    raise ValueError("User not found.")
                # Compare and update details if necessary
                if current_user_data['slots'] != user.get('slots') or current_user_data['areaId'] != user.get('area_id'):
                    change_tutor_details(cur, user)
                if current_user_data['type'] != user.get('type'):
                    # User type has changed.
                    if user['type'] == "student":
                        delete_old_expertises(cur, user)
                        conn.commit()
                        change_user_type_db(user['id'], user['type'])
                    else:
                        delete_old_expertises(cur, user)
                        add_new_expertises(cur, user)
                        conn.commit()
                        change_user_type_db(user['id'], user['type'])
                else:
                    delete_old_expertises(cur, user)
                    add_new_expertises(cur, user)
                    conn.commit()
            return True, "User updated successfully"
    except ValueError as e:
        conn.rollback()  
        return False, str(e)  
    except Exception as e:
        conn.rollback()  
        return False, f"Unexpected error: {e}"
    finally:
        DBPool.get_instance().putconn(conn)

def delete_old_user(cur, oldType, id):
    try:
        cur.execute(f"DELETE FROM {oldType} WHERE user_id = %s", ( id,))
    except Exception as e:
        raise ValueError(f"Error deleting old user: {e}")

def delete_old_expertises(cur, user):
    try:
        cur.execute("DELETE FROM tutor_expertise WHERE tutor_id = %s", (user['tutor_id'],))
    except Exception as e:
        raise ValueError(f"Error deleting old expertises: {e}")

def change_tutor_details(cur, user):
    try:
        cur.execute("UPDATE tutors SET slots = %s, area_id = %s WHERE id = %s", 
                    (user['slots'], None if user['area_id'] == 0 else user['area_id'], user['tutor_id']))
        affected_rows = cur.rowcount
    except Exception as e:
        raise ValueError(f"Error updating tutor details: {e}")
    
def add_new_expertises(cur, user):
    try:
        for expertise_id in user['expertises']:
            cur.execute("INSERT INTO tutor_expertise (tutor_id, expertise_id) VALUES (%s, %s)", 
                        (user['tutor_id'], expertise_id))
    except Exception as e:
        raise ValueError(f"Error adding new expertises: {e}")

def get_user_credentials(email):
    if not email:
        return False, "Email is required."
    with DBPool.get_instance().getconn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute('SELECT id, password, type FROM "users" WHERE email = %s', (email,))
                result = cur.fetchone()
                if result:
                    user_id, stored_password, user_type = result
                    print("Password verified for user ID: ", user_id, file=sys.stderr)
                    encoded_password = stored_password.encode('utf-8') if isinstance(stored_password, str) else stored_password
                    return (user_id, encoded_password, user_type)
                else:
                    return False, "User not found."
            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
                return False, "An error occurred while fetching user credentials."
            finally:
                DBPool.get_instance().putconn(conn)

def fetch_current_user_data(cur, user_id):
    cur.execute("""
                    SELECT u.id, t.id, u.firstName, u.lastName, u.email, u.type, COALESCE(t.slots, '0') AS slots, COALESCE(a.id, '0') AS areaId
                    FROM "users" u
                    LEFT JOIN "tutors" t ON u.id = t.user_id
                    LEFT JOIN "areas" a ON t.area_id = a.id
                    WHERE u.id = %s
                """,(user_id,)) 
    user = cur.fetchone()
    if user:
        cur.execute("""
                            SELECT *
                            FROM "tutor_expertise" te
                            LEFT JOIN "expertises" e ON te.expertise_id = e.id
                            WHERE te.tutor_id = %s
                        """, (user[1],))
        expertises_results = cur.fetchall()
        if expertises_results:
            expertises = [expertise[0] for expertise in expertises_results]
        else:
            expertises = []
        return {
            'id': user[0],
            'tutor_id': user[1],
            'firstName': user[2],  
            'lastName': user[3],   
            'email': user[4],
            'type': user[5],
            'slots': user[6],
            'areaId': user[7],
            'expertises': expertises
            }
    else:
        return None

def add_project(project):

    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                conn.autocommit = False    
                project_id, success = store_projects_in_database(project['name'], project['description'], project['student_id'], project['tutor_id'], project['area_id'])
                try:
                    for expertise_id in project['expertises']:
                        cur.execute("INSERT INTO project_expertise (project_id, expertise_id) VALUES (%s, %s)", 
                                    (project_id, expertise_id))
                except Exception as e:
                    raise ValueError(f"Error adding new expertises: {e}")
                conn.commit()                    
            return True, "project added successfully"
    except ValueError as e:
        conn.rollback() 
        return False, str(e)  
    except Exception as e:
        conn.rollback()  
        return False, f"Unexpected error: {e}"
    finally:
        DBPool.get_instance().putconn(conn)

def update_project(project_id, student_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        UPDATE "projects"
                        SET student_id = %s, alocated = true
                        WHERE id = %s;
                    """, (student_id, project_id))
                    conn.commit()

                    if cur.rowcount == 0:
                        return False, "project not found"
            
                    return True, "project selected successfully"

                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to change project:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def findTutors(project, tutors):
    match_percentages = []
    for tutor in tutors:
        if tutor["area_id"] == project["area_id"] and tutor["slots"] > 0:
            matched_expertises = set(tutor["expertises"]).intersection(set(project["expertises"]))
            match_percentage = len(matched_expertises) / len(project["expertises"])
            match_percentages.append({"tutor_id": tutor["tutor_id"], "match_percentage": match_percentage})
    match_percentages.sort(key=lambda x: x["match_percentage"], reverse=True)
    return match_percentages

def update_new_tutor(project):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        UPDATE "projects"
                        SET tutor_id = %s, alocated = true
                        WHERE id = %s;
                    """, (project["tutor_id"], project["id"]))
                    conn.commit()

                    if cur.rowcount == 0:
                        return False, "project not found"
            
                    return True, "project updated successfully"

                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to change project:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)
            
def change_user_password(email, password):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        UPDATE "users"
                        SET password = %s
                        WHERE email = %s;
                    """, (password, email))
                    conn.commit()

                    if cur.rowcount == 0:
                        return False, "user not found"
            
                    return True, "password updated successfully"

                except psycopg2.Error as e:
                    conn.rollback() 
                    return f"Failed to change project:", 500
                except Exception as e:
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def change_Project(project):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                conn.autocommit = False  
                cur.execute("""
                    UPDATE "projects"
                    SET name = %s, description = %s, student_id = %s, tutor_id = %s, area_id = %s, alocated = %s
                    WHERE id = %s;
                """, (project['name'], project['description'], project['student_id'], project['tutor_id'], project['area_id'], project['alocated'], project['id']))
                
                cur.execute("""
                    DELETE FROM "project_expertise"
                    WHERE project_id = %s;
                """, (project['id'],))

                for expertise_id in project['expertises']:
                    cur.execute("""
                        INSERT INTO "project_expertise" (project_id, expertise_id) VALUES (%s, %s)
                    """, (project['id'], expertise_id))

                conn.commit()
                return True, "Project updated successfully"
    except ValueError as e:
        conn.rollback()  
        return False, str(e)  
    except Exception as e:
        conn.rollback() 
        return False, f"Unexpected error: {e}"
    finally:
        DBPool.get_instance().putconn(conn)

    
    
#Creat mock data to use the app
def createDefaultData():
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM \"users\"")
                user = cur.fetchone()
                if not user:
                    logger.info('loading mock data')
                    load_mock_data()
                    logger.info('Mock data Loaded')
    except Exception as e:
        logger.exception("Error fetching users: %s", e)
    finally:
        if conn:
            DBPool.get_instance().putconn(conn)

def insert_data(db_pool, table_name, data):
    columns = ', '.join(data[0].keys())
    placeholders = ', '.join(['%s'] * len(data[0]))
    sql = f"INSERT INTO \"{table_name}\" ({columns}) VALUES ({placeholders})"
    
    with db_pool.get_instance().getconn() as conn:
        with conn.cursor() as cur:
            for item in data:
                values = tuple(item.values())
                cur.execute(sql, values)
            conn.commit()

def load_mock_data():
    with open('mock_data.json', 'r') as file:
        mock_data = json.load(file)
    
    insert_data(DBPool, 'areas', mock_data['areas'])
    insert_data(DBPool, 'expertises', mock_data['expertises'])
    insert_data(DBPool, 'users', mock_data['users'])
    insert_data(DBPool, 'tutors', mock_data['tutors'])
    insert_data(DBPool, 'students', mock_data['students'])
    insert_data(DBPool, 'projects', mock_data['projects'])
    insert_data(DBPool, 'tutor_expertise', mock_data['tutor_expertise'])
    insert_data(DBPool, 'project_expertise', mock_data['project_expertise'])

    print("Mock data inserted successfully.")

