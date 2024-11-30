# Interview Slot Management System

This project is a Django-based application that facilitates the management of interview time slots. It allows candidates and interviewers to register their availability and provides a feature to find overlapping 1-hour time slots for scheduling interviews.


## Installation

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate # on linux
venv\Scripts\activate # on windows
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run the development server:

```bash
python manage.py runserver
```

## API Endpoints

### 1. Register Time Slots
### `/slot (POST)`
Registers availability for a candidate or interviewer
```bash
# payload
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "user_type": "candidate",
    "date": "2024-12-01",
    "from_time": "10:00:AM",
    "to_time": "02:00:PM"
}
```

### 2. Get Available Slots
### `/slot (GET)`
Retrieves 1-hour overlapping slots between a candidate and an interviewer
```bash
# parameters
candidate: Candidate user id
interviewer: Interviewer user id
```

