# AI-Based Project Allocation System

This repository contains the source code for an AI-based project allocation system, designed to connect students and tutors for project collaboration. This system allows users to create accounts, browse proposed projects by tutors, and manage their own project ideas.

## Features

- User authentication (Sign in & Sign up)
- Project browsing and allocation
- Dashboard for project management

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Node.js installed (v14.x or later)
- Python installed (v3.8 or later)
- Docker and Docker Compose installed

## Technology Stack

- **Frontend**: Vue.js
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker

## Setup

Clone the repository to your local machine:

```bash
git clone https://github.com/Guildb/AI_Based_Project_Allocation.git
cd AI_Based_Project_Allocation
```

Using Docker
This project is configured to run using Docker and Docker Compose for ease of setup and reliability across different environments:

open Docker Desktop

Build and Run the ContainersNavigate to the root directory of the project and run:
```bash
docker-compose up --build
```
This command builds the images and starts the containers necessary for the backend, frontend, and database.
Access the ApplicationAfter all containers are up and running, you can access the application through:
Frontend: http://localhost:8080
Backend (API): http://localhost:5000
