
# User Authentication & JWT

A secure backend authentication application developed using Python Flask.

## Features
- User registration
- User login
- Bcrypt password hashing
- JWT token generation
- JWT-protected profile API
- SQLite database
- Duplicate email prevention
- Input validation

## Tech Stack
- Python
- Flask
- SQLite
- Flask-Bcrypt
- Flask-JWT-Extended
- Gunicorn

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API information |
| GET | /health | Health check |
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login user |
| GET | /api/auth/profile | Protected profile |

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

## Developer
Aryan Jain


## Live Demo

**Deployed Backend URL:**

https://user-auth-jwt-vk1k.onrender.com

**Health Check:**

https://user-auth-jwt-vk1k.onrender.com/health

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Backend status |
| GET | /health | Health check |
| POST | /api/auth/register | User registration |
| POST | /api/auth/login | User login |
| GET | /api/auth/profile | Protected profile |

## Testing Results

- User Registration: Passed
- User Login: Passed
- JWT Generation: Passed
- Protected Profile: Passed
- Wrong Password: Passed
- Unauthorized Access: Passed
