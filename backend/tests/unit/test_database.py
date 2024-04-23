import unittest
from unittest.mock import MagicMock, patch
from database import *


class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('database.DBPool.get_instance')
        mock_get_instance = self.patcher.start()
        
        # Mock the connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cur = MagicMock()
        mock_get_instance.return_value.getconn.return_value = self.mock_conn
        self.mock_conn.__enter__.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cur

    def tearDown(self):
        self.patcher.stop()
        
    
    # table users    
    def test_create_table_users_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_users_if_not_exists()
        self.assertEqual("Table 'users' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_users_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_users_if_not_exists()
        self.assertEqual("Table 'users' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "users" (
                            id SERIAL PRIMARY KEY,
                            firstName VARCHAR(255) NOT NULL,
                            lastName VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL UNIQUE,
                            password VARCHAR(255) NOT NULL,
                            type VARCHAR(255) NOT NULL
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_users_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_users_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table areas
    def test_create_table_areas_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_areas_if_not_exists()
        self.assertEqual("Table 'areas' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'areas')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_areas_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_areas_if_not_exists()
        self.assertEqual("Table 'areas' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "areas" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL UNIQUE
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_areas_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_areas_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table expertises
    def test_create_table_expertises_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_expertises_if_not_exists()
        self.assertEqual("Table 'expertises' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'expertises')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_expertises_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_expertises_if_not_exists()
        self.assertEqual("Table 'expertises' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "expertises" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            acronym VARCHAR(255) NOT NULL,
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_expertises_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_expertises_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table tutors
    def test_create_table_tutors_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_tutors_if_not_exists()
        self.assertEqual("Table 'tutors' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tutors')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_tutors_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_tutors_if_not_exists()
        self.assertEqual("Table 'tutors' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "tutors" (
                            id SERIAL PRIMARY KEY,
                            slots INTEGER NOT NULL,
                            user_id INTEGER REFERENCES "users" (id),
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_tutors_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_tutors_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table students
    def test_create_table_students_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_students_if_not_exists()
        self.assertEqual("Table 'students' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'students')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_students_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_students_if_not_exists()
        self.assertEqual("Table 'students' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "students" (
                            id SERIAL PRIMARY KEY,
                            student_number VARCHAR(255) NOT NULL,
                            user_id INTEGER REFERENCES "users" (id),
                            area_id INTEGER REFERENCES "areas" (id)
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_students_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_students_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table projects
    def test_create_table_projects_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_projects_if_not_exists()
        self.assertEqual("Table 'projects' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'projects')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_projects_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_projects_if_not_exists()
        self.assertEqual("Table 'projects' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "projects" (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            description VARCHAR(255) NOT NULL,
                            student_id INTEGER REFERENCES "students" (id),
                            tutor_id INTEGER REFERENCES "tutors" (id),
                            area_id INTEGER REFERENCES "areas" (id),
                            alocated BOOLEAN NOT NULL DEFAULT FALSE
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_projects_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_projects_if_not_exists()
        self.assertIn("Unable to create table:", response)
  
    #table tutor_expertise
    def test_create_table_tutor_expertise_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_tutor_expertise_if_not_exists()
        self.assertEqual("Table 'tutor_expertise' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tutor_expertise')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_tutor_expertise_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_tutor_expertise_if_not_exists()
        self.assertEqual("Table 'tutor_expertise' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "tutor_expertise" (
                            id SERIAL PRIMARY KEY,
                            tutor_id INTEGER REFERENCES "tutors" (id),
                            expertise_id INTEGER REFERENCES "expertises" (id)
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_tutor_expertise_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_tutor_expertise_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #table project_expertise
    def test_create_table_project_expertise_if_not_exists_already_exists(self):
        # Setup the cursor’s fetchone method to simulate that the table already exists
        self.mock_cur.fetchone.return_value = (True,)

        response = create_table_project_expertise_if_not_exists()
        self.assertEqual("Table 'project_expertise' already exists.", response)
        self.mock_cur.execute.assert_called_once_with("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'project_expertise')")
        self.mock_conn.commit.assert_not_called()
        
    def test_create_table_project_expertise_if_not_exists_creates_successfully(self):
        # Setup the cursor’s fetchone method to simulate that the table does not exist
        self.mock_cur.fetchone.return_value = (False,)

        response = create_table_project_expertise_if_not_exists()
        self.assertEqual("Table 'project_expertise' created successfully.", response)
        # Check SQL execution for table creation
        expected_sql = """
                        CREATE TABLE "project_expertise" (
                            id SERIAL PRIMARY KEY,
                            project_id INTEGER REFERENCES "projects" (id),
                            expertise_id INTEGER REFERENCES "expertises" (id)
                        )
                    """
        self.mock_cur.execute.assert_any_call(expected_sql)
        self.mock_conn.commit.assert_called_once()
    
    def test_create_table_project_expertise_if_not_exists_exception_handling(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Mocked error")
        response = create_table_project_expertise_if_not_exists()
        self.assertIn("Unable to create table:", response)

    #add data to tables
    ## user table
    def test_store_user_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_user_in_database("John", "Doe", "john@example.com", "hashed_password", "type")
        self.assertIsNone(response)
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "users" (firstName, lastName, email, password, type)
                        VALUES (%s, %s, %s, %s, %s)
                    """,
            ("John", "Doe", "john@example.com", "hashed_password", "type")
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_user_in_database_unique_violation(self):
        self.mock_cur.execute.side_effect = psycopg2.errors.UniqueViolation
        response = store_user_in_database("John", "Doe", "john@example.com", "hashed_password", "type")
        self.assertEqual(response, ("Email address already exists.", 409))

    ## area table
    def test_store_area_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_areas_in_database("Test Area")
        self.assertEqual(response, ("Area stored successfully.", 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "areas" (name)
                        VALUES (%s)
                    """, ("Test Area",)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_area_in_database_unique_violation(self):
        self.mock_cur.execute.side_effect = psycopg2.errors.UniqueViolation
        response = store_areas_in_database("Test Area")
        self.assertEqual(response, ("Failed to insert area: Area already exists.", 409))

    ## expertises table
    def test_store_expertises_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_expertises_in_database("Test Expertise", "TE", 1)
        self.assertEqual(response, (None, 201))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "expertises" (name, acronym, area_id)
                        VALUES (%s, %s, %s)
                    """,("Test Expertise", "TE", 1)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_expertises_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error
        response = store_expertises_in_database("Test Expertise", "TE", 1)
        self.assertEqual(response, ("Failed to insert expertise:", 500))
        self.mock_conn.rollback.assert_called_once()

    ## tutors table
    def test_store_tutors_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_tutors_in_database(5, 1, 1)
        self.assertEqual(response, ("tutor stored successfully.", 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "tutors" (slots, user_id, area_id)
                        VALUES (%s, %s, %s)
                    """,(5, 1, 1)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_tutors_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error
        response = store_tutors_in_database(5, 1, 1)
        self.assertEqual(response, ("Failed to insert tutor:", 500))
        self.mock_conn.rollback.assert_called_once()

    ## students table
    def test_store_students_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_students_in_database("student_number", 1, 1)
        self.assertEqual(response, ("student stored successfully.", 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "students" (student_number, user_id, area_id)
                        VALUES (%s, %s, %s)
                    """, ("student_number", 1, 1))
        self.mock_conn.commit.assert_called_once()

    def test_store_students_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error
        response = store_students_in_database("student_number", 1, 1)
        self.assertEqual(response, ("Failed to insert student:", 500))
        self.mock_conn.rollback.assert_called_once()

    ## tutor_expertise table
    def test_store_tutor_expertise_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_tutor_expertise_in_database(1, 1)
        self.assertEqual(response, ("tutor_expertise stored successfully.", 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "tutor_expertise" (tutor_id, expertise_id)
                        VALUES (%s, %s)
                    """, (1, 1)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_tutor_expertise_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error
        response = store_tutor_expertise_in_database(1, 1)
        self.assertEqual(response, ("Failed to insert tutor_expertise:", 500))
        self.mock_conn.rollback.assert_called_once()

    ## project table
    def test_store_projects_in_database_success(self):
        self.mock_cur.execute.return_value = None
        self.mock_cur.fetchone.return_value = (1,)
        response = store_projects_in_database("Project 1", "Description", 1, 2, 3)
        self.assertEqual(response, (1, 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "projects" (name, description, student_id, tutor_id, area_id, alocated)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """,
            ("Project 1", "Description", 1, 2, 3, True)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_projects_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error("Some error")
        response = store_projects_in_database("Project 1", "Description", 1, 2, 3)
        self.assertEqual(response, ("Failed to insert project:", 500))
        self.mock_conn.rollback.assert_called_once()

    ## project_expertise table
    def test_store_project_expertise_in_database_success(self):
        self.mock_cur.execute.return_value = None
        response = store_project_expertise_in_database(1, 1)
        self.assertEqual(response, ("project_expertise stored successfully.", 200))
        self.mock_cur.execute.assert_called_once_with(
            """
                        INSERT INTO "project_expertise" (project_id, expertise_id)
                        VALUES (%s, %s)
                    """, (1,1)
        )
        self.mock_conn.commit.assert_called_once()

    def test_store_project_expertise_in_database_failure(self):
        self.mock_cur.execute.side_effect = psycopg2.Error
        response = store_project_expertise_in_database(1, 1)
        self.assertEqual(response, ("Failed to insert project_expertise:", 500))
        self.mock_conn.rollback.assert_called_once()

    # deleting data from tables
    ## student table
    def test_delete_student_success(self):
        self.mock_cur.execute.return_value = None
        response, message = delete_student({'student_id': 1, 'id': 1})
        self.assertTrue(response)
        self.assertEqual(message, 'Student deleted successfully')
        self.mock_cur.execute.assert_any_call(
            """
                                UPDATE "projects"
                                SET student_id = null, alocated = False
                                WHERE student_id = %s;
                                """,
            (1,)
        )
        self.mock_cur.execute.assert_any_call("DELETE FROM students WHERE user_id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM users WHERE id = %s", (1,))

        # Verify that the connection's commit method was called
        self.mock_conn.commit.assert_called_once()

    ## tutor table 
    def test_delete_tutor_success(self):
        self.mock_cur.execute.return_value = None
        user = {'tutor_id': 1, 'id': 1}
        response, message = delete_tutor(user)
        self.assertTrue(response)
        self.assertEqual(message, 'Tutor deleted successfully')
        self.mock_cur.execute.assert_any_call(
            """
                                UPDATE "projects" 
                                SET tutor_id = null, alocated = False 
                                WHERE tutor_id = %s; 
                                """,
            (1,)
        )
        self.mock_cur.execute.assert_any_call("DELETE FROM tutor_expertise WHERE tutor_id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM tutors WHERE id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM users WHERE id = %s", (1,))

        # Verify that the connection's commit method was called
        self.mock_conn.commit.assert_called_once()

    ## area table
    def test_delete_area_success(self):
        self.mock_cur.execute.return_value = None
        area_id = 1
        response, message = delete_area(area_id)
        self.assertTrue(response)
        self.assertEqual(message, 'Area deleted successfully')
        self.mock_cur.execute.assert_any_call(
            """UPDATE "projects" SET area_id = null WHERE area_id = %s; """,
            (1,)
        )
        self.mock_cur.execute.assert_any_call("DELETE FROM areas WHERE id = %s", (1,))
        self.mock_conn.commit.assert_called_once()

    ## expertise table
    def test_delete_expertise_success(self):
        self.mock_cur.execute.return_value = None
        expertise_id = 1
        response, message = delete_expertise(expertise_id)
        self.assertTrue(response)
        self.assertEqual(message, 'Expertise and related associations deleted successfully')
        self.mock_cur.execute.assert_any_call("DELETE FROM tutor_expertise WHERE expertise_id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM project_expertise WHERE expertise_id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM expertises WHERE id = %s", (1,))

        # Verify that the connection's commit method was called
        self.mock_conn.commit.assert_called_once()

    ## project table
    def test_delete_project_success(self):
        self.mock_cur.execute.return_value = None
        project_id = 1
        response, message = delete_project(project_id)
        self.assertTrue(response)
        self.assertEqual(message, 'Tutor deleted successfully')
        self.mock_cur.execute.assert_any_call("DELETE FROM project_expertise WHERE project_id = %s", (1,))
        self.mock_cur.execute.assert_any_call("DELETE FROM projects WHERE id = %s", (1,))
        self.mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
