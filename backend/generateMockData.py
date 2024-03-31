import json
import random

# Mock data generation
users = [
    {
        "firstName": f"FirstName{i}",
        "lastName": f"LastName{i}",
        "email": f"user{i}@example.com",
        "password": "password",
        "type": random.choice(["student", "tutor", "courseLeader"])
    } for i in range(1, 11)
]

areas = [
    {"name": f"Area {i}"} for i in range(1, 6)
]

expertises = [
    {
        "name": f"Expertise {i}",
        "acronym": f"EXP{i}",
        "area_id": random.randint(1, 5)
    } for i in range(1, 11)
]

tutors = [
    {
        "slots": random.randint(1, 5),
        "user_id": i,
        "area_id": random.randint(1, 5)
    } for i in range(2, 7)  # Assuming some users are tutors
]

students = [
    {
        "student_number": f"S{i:03}",
        "user_id": i
    } for i in range(7, 12)  # Assuming some users are students
]

projects = [
    {
        "name": f"Project {i}",
        "description": f"Project description {i}",
        "student_id": random.randint(1, 5),
        "tutor_id": random.randint(1, 5),
        "area_id": random.randint(1, 5),
        "alocated": random.choice([True, False])
    } for i in range(1, 11)
]

# Combine all mock data into a single dictionary
mock_data = {
    "users": users,
    "areas": areas,
    "expertises": expertises,
    "tutors": tutors,
    "students": students,
    "projects": projects
}

# Convert mock data to JSON and save to a file
with open('mock_data.json', 'w') as json_file:
    json.dump(mock_data, json_file, indent=2)
