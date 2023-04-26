from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from datetime import datetime, timedelta
import secrets
import bcrypt
import jwt

app = FastAPI()


# Allow CORS for development purposes
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with the domains you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="Resumebuilder",
    user="postgres",
    password="Tvans@527"
)

# User model


class User(BaseModel):
    email: str
    password: str
    name: str
    
# LoginUser model


class LoginUser(BaseModel):
    email: str
    password: str


# Get JWT token from header



# Verify JWT token and get current user



# Sign up new user


@app.post("/signup")
def signup(user: User):
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT email FROM users WHERE email=%s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Insert user into database
    cursor.execute(
        "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)",
        (user.email, hashed_password.decode(),
         user.name)
    )
    conn.commit()

    return {"message": "User created successfully"}

# Log in existing user and generate JWT token


@app.post("/login")
def login(user: LoginUser):
    cursor = conn.cursor()

    # Retrieve user from database
    cursor.execute(
        "SELECT email, password, name FROM users WHERE email=%s", (user.email,))
    db_user = cursor.fetchone()

    if db_user is None:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")

    # Verify password
    if bcrypt.checkpw(user.password.encode(), db_user[1].encode()):
        # Generate JWT token
        # Decode JWT token to get user email
        if user.email is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")

        # Retrieve user details from database
        cursor.execute(
            "SELECT email, name FROM users WHERE email=%s", (user.email,))
        current_user = cursor.fetchone()

        return {"access_token": current_user}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")



