# Cloud Provider Recommender

Cloud Provider Recommender is a web application developed with Django that provides personalized cloud service provider recommendations based on users’ specific requirements.  
The project combines machine learning techniques with secure web functionalities to deliver a smooth and intelligent user experience.

---

## Project Description

Project Name: Cloud Provider Recommender

This application allows users to enter their technical and financial requirements (storage, CPU, budget, encryption support, service model score, and activity field) in order to automatically receive the most suitable cloud provider.  
Recommendations are generated using a Machine Learning algorithm (Nearest Neighbors) based on a CSV dataset.

---

## Main Features

### User Registration and Authentication
- Registration form with validation
- Secure login and session management
- Custom password reset functionality

### Recommendation Form
- Users provide their requirements:
  - Storage
  - CPU
  - Budget
  - Encryption support
  - Service model score
  - Activity field
- Recommendation based on the Nearest Neighbors algorithm
- Uses the dataset file `cloud_data_10000.csv`
- Recommendations are stored in the database for later review

### Admin Dashboard
- Accessible only to superusers
- View all generated recommendations
- Delete irrelevant or outdated recommendations

### User Experience
- Responsive interface built with Bootstrap 5
- Real-time success and error messages
- Client-side form validation for better usability

### Security
- Secure authentication with privilege control
- Isolated user sessions
- View protection using Django decorators:
  - `@login_required`
  - `@staff_member_required`

---

## Technologies Used

- Backend: Python, Django
- Machine Learning: scikit-learn  
  - NearestNeighbors  
  - StandardScaler
- Frontend: HTML, Bootstrap 5, Django Templates
- Database: SQLite / PostgreSQL
- Forms Management: Django Forms
- User Messages: Django Messages Framework

---

## Installation and Setup

### Create and activate a virtual environment :
python -m venv venv
venv\Scripts\activate 

### Install dependencies  :
pip install Django pandas scikit-learn numpy python-dateutil pytz sqlparse

### Then, you can run  :
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

### Access the application :
Application: http://127.0.0.1:8000/
Admin panel: http://127.0.0.1:8000/admin/



