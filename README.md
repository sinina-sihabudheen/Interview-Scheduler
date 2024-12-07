Interview Scheduling API

This is a Django-based API for scheduling interviews between candidates and interviewers. The API allows candidates and interviewers to register their available time slots and check for overlapping time slots to schedule an interview.

Requirements

System Requirements:
  Python 3.8 or higher
  Django 5.0 or higher
  Django Rest Framework
  Database (PostgreSQL)
  Docker for containerization
Python Dependencies:
  This project uses the following Python libraries:
    Django: Framework for building the backend API.
    Django REST Framework: For building the API views and handling HTTP requests.
    psycopg2: For PostgreSQL database connection (if using PostgreSQL).
    docker: For containerizing the application.

You can install all the dependencies by running the following command:
  pip install -r requirements.txt

For Docker, build the image using the following command:
docker-compose up --build

Setting Up the Project
Clone the repository:
  **git clone (https://github.com/sinina-sihabudheen/Interview-Scheduler.git)**
  cd interview_scheduler
  
Configure the Database:
  Ensure the database is properly set up (PostgreSQL).
  Update the DATABASES setting in settings.py 


API Endpoints

1. Register Candidate
  URL: /api/interviews/register_candidate/
  Method: POST
  Description: Registers a candidate with basic information .
  Request Body:
      {
      "name": "Candidate1",
      "email": "candidate1@example.com",
      "available_dates": ["2024-12-10", "2024-12-11"],
      "available_times": [["08:00-9:00", "11:00-12:00"], ["10:00-11:00"]]
      }

2. Register Interviewer
  URL: /api/interviews/register_interviewer/
  Method: POST
  Description: Registers an interviewer with basic information (name, email, etc.).
  Request Body:
    {
    "name": "Interviewer1",
    "email": "interviewer1@example.com",
    "available_dates": ["2024-12-10", "2024-12-11"],
    "available_times": [["08:00-9:00", "11:00-12:00"], ["10:00-11:00"]]
    }
3. Get Available Slots
  URL: /api/interviews/get_available_slots/
  Method: GET
  Description: Retrieves the available interview slots for a specific candidate and interviewer based on overlapping availability.
  Query Parameters:
    candidate_id: The ID of the candidate.
    interviewer_id: The ID of the interviewer.

