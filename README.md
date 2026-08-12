# Interview Platform — OOP Learning Project

## Overview

A CLI-based interview platform built with Python, PostgreSQL, and Docker.
The project was developed to practice Object-Oriented Programming concepts
while building a small real-world application.

The system supports three user roles:

- Candidate
- Interviewer
- Admin

Users interact with the application through a CLI, while PostgreSQL stores
persistent application data.

## Features

### Candidate

- Sign up and log in
- Apply for an interview
- Receive a randomly assigned interviewer
- View interview history

### Interviewer

- Log in
- View assigned candidates
- Mark interviews as completed

### Admin

- Create an admin account through the setup script
- View all users
- Delete user accounts

## Technologies

- Python
- PostgreSQL
- Docker / Docker Compose
- Pytest
- Git / GitHub

## OOP Concepts

- **Inheritance** — Candidate, Interviewer, and Admin inherit from User
- **Encapsulation** — Database operations are handled by the Database class
- **Polymorphism** — Role-specific classes provide their own behavior
- **Abstraction** — Application logic is separated into appropriate classes
- **super()** — Child classes use the parent constructor where required

## Project Structure

```text
interview_system/
├── models/
│   ├── user.py
│   ├── candidate.py
│   ├── interviewer.py
│   └── admin.py
├── tests/
├── database.py
├── main.py
├── setup_admin.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .gitignore
Database

The application uses PostgreSQL with two main tables.

Users

Stores user information and their roles.

id
name
email
password
role
Interviews

Stores candidate/interviewer relationships and interview status.

id
candidate_id → users.id
interviewer_id → users.id
status

Foreign keys are used to establish relationships between users and interviews.

Running the Project
1. Start the Containers
docker compose up -d
2. Create an Admin Account
docker compose exec app python setup_admin.py
3. Run the Application
docker compose exec app python main.py
4. Run Tests
docker compose exec app python -m pytest tests/ -v
5. Stop the Containers
docker compose down

To stop the containers and remove the database volume:

docker compose down -v
Testing

The project includes pytest tests covering:

Database operations
User functionality
OOP behavior
Interview workflow
Input validation

Tests use cleanup mechanisms to avoid leaving test data behind.

Learning Objectives

This project was built to practice:

Object-Oriented Programming
Inheritance and super()
Database design and SQL
Python → PostgreSQL integration
Docker and containerized development
Automated testing with pytest
Git-based development workflow
Future Improvements

Potential improvements include:

Password hashing
More robust input validation
Interview scheduling
Additional interview workflow features
Logging and auditing

Built as part of OOP learning — Week 3-4