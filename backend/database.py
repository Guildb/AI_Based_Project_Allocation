import psycopg2
from psycopg2 import pool
import jwt
import datetime
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__) 
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
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
                            user_id INTEGER REFERENCES "users" (id)
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
                            expertise_id INTEGER REFERENCES "expertises" (id),
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
                    return None  # User stored successfully
                except psycopg2.errors.UniqueViolation as e:
                    logger.error("Duplicate email address", exc_info=True)
                    return "Email address already exists.", 409
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert user: {e}", exc_info=True)
                    conn.rollback()  # Rollback the transaction on error
                    return "Failed to insert user.", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")
                    conn.rollback()  # Rollback the transaction on error
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
                    return "Area stored successfully."
                except psycopg2.errors.UniqueViolation as e:
                    logger.error("Duplicated area", exc_info=True)
                    return "Failed to insert area: Area already exists.", 409
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert area: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to insert area:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
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
                cur.execute("""
                    INSERT INTO "expertises" (name, acronym, area_id)
                    VALUES (%s, %s, %s)
                """, (name, acronym, area_id))
                conn.commit()
                print("Expertise stored successfully")
                # Success: Return None for error message and 201 for status code
                return None, 201
    except psycopg2.Error as e:
        logger.error(f"Failed to insert expertise: {e}", exc_info=True)
        # Rollback the transaction on error
        conn.rollback() 
        # Error: Return error message and 500 for status code
        return "Failed to insert expertise due to a database error.", 500
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        conn.rollback() 
        # Error: Return error message and 500 for status code
        return "Unexpected error occurred.", 500
    finally:
        DBPool.get_instance().putconn(conn)

# Adjust the `except` at the outer level if needed, based on your application's error handling strategy


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
                    return "tutor stored successfully."
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert tutor: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to insert tutor:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add tutor: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_students_in_database(student_number, user_id):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "students" (student_number, user_id)
                        VALUES (%s, %s)
                    """, (student_number, user_id))
                    conn.commit()
                    print("student stored successfully")
                    return "student stored successfully."
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert student: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to insert student:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
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
                    return "tutor_expertise stored successfully."
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert tutor_expertise: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to insert tutor_expertise:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def store_projects_in_database(name, description, student_id, tutor_id, area_id, expertise_id, alocated):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO "projects" (name, description, student_id, tutor_id, area_id, expertise_id, alocated)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (name, description, student_id, tutor_id, area_id, expertise_id, alocated))
                    conn.commit()
                    print("project stored successfully")
                    return "project stored successfully."
                except psycopg2.Error as e:
                    logger.error(f"Failed to insert project: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to insert project:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to add project: {e}"
    finally:
            DBPool.get_instance().putconn(conn)
       
def change_user_type_in_database(userId, newType):
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
                    logger.error(f"Failed to change type: {e}", exc_info=True)  # Log the error with stack trace
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Failed to change type:", 500
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")  # Log unexpected errors with full context 
                    # Rollback the transaction on error
                    conn.rollback() 
                    return f"Unexpected error: {e}", 500
    except psycopg2.Error as e:
        return f"Unable to create link: {e}"
    finally:
            DBPool.get_instance().putconn(conn)

def update_user(user):
    try:
        with DBPool.get_instance().getconn() as conn:
            with conn.cursor() as cur:
                try:
                    conn.autocommit = False  # Disable autocommit for transaction control

                    # Perform database operations
                    change_tutor_details(cur, user)
                    change_tutor_type(cur, user)
                    delete_old_expertises(cur, user)
                    add_new_expertises(cur, user)

                    conn.commit()  # Commit the transaction if all operations succeed
                    return True, "User updated successfully"  # Indicate success
                except psycopg2.Error as e:
                    conn.rollback()  # Rollback the transaction in case of a database error
                    return False, f"Transaction failed: {e}"  # Indicate failure and return error message
                except Exception as e:
                    conn.rollback()  # Rollback the transaction in case of a general error
                    return False, f"Unexpected error: {e}"  # Indicate failure and return error message
    except psycopg2.Error as e:
        return False, f"Unable to create link: {e}"  # Return False for failure outside the inner try-except
    finally:
        DBPool.get_instance().putconn(conn)  # Ensure the connection is always returned to the pool


def change_tutor_details(cur, user):
    cur.execute("UPDATE tutors SET slots = %s, area_id = %s WHERE id = %s", (user['slots'], user['areaId'] , user['id']))

def delete_old_expertises(cur, user):
    cur.execute("DELETE FROM tutor_expertise WHERE tutor_id = %s", ( user['tutor_id'],))

def add_new_expertises(cur, user):
    for e in user['expertises']:
        cur.execute("INSERT INTO tutor_expertise (tutor_id, expertise_id) VALUES (%s, %s)", (user['tutor_id'], e['id']))

def change_tutor_type(cur, user):
    cur.execute("UPDATE users SET type = %s WHERE id = %s", (user['type'], user['id']))

 
           






def insert_default_data():
    store_user_in_database("defaultuser", "defaultuser","defaultuser","defaultuser")
    store_areas_in_database("defaultarea")
    store_expertises_in_database("defaultexpertise","defaultexpertise",1)
    store_tutors_in_database(5, 1,1)
    store_students_in_database("defaultstudent", 1)
    store_tutor_expertise_in_database(1,1)
    store_projects_in_database("defaultProject","defaultProject",1,1,1,1,True)

