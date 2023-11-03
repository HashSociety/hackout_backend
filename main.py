from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, CHAR
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()


# -------------- For MySQL --------------

# DATABASE_URL = "mysql+mysqlconnector://your_username:your_password@your_host/your_database"
# database = Database(DATABASE_URL)
# metadata = database.metadata

# Base = declarative_base()

# metadata.create_all(bind=create_engine(DATABASE_URL))

# -------------- testing using sqllite --------------

conn: sqlite3.Connection = sqlite3.connect("test.db")

conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        last_name TEXT,
        gender CHAR,
        email TEXT,
        password TEXT
    )
''')


conn.execute('''
    CREATE TABLE IF NOT EXISTS form_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        destination TEXT,
        group_size INTEGER,
        transportation_method TEXT
    )
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS chat_rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT,
        room_size INTEGER,
        admin_user_id INTEGER
    )
''')

# -------------- Classes --------------

class UserCreate(BaseModel):
    username: str
    name: str
    last_name: str
    gender: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

class FormData(BaseModel):
    destination: str
    group_size: int
    transportation_method: str


class RoomCreate(BaseModel):
    user_id: int
    room_name: str
    room_size: int
    room_id: int
    room_type: str

# -------------- login Signup --------------

@app.post("/register/", response_model=UserCreate)
async def register_user(user: UserCreate):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, name, last_name, gender, email, password) VALUES (?, ?, ?, ?, ?, ?)",
        (user.username, user.name, user.last_name, user.gender, user.email, user.password),
    )
    conn.commit()
    cursor.close()
    return user


@app.post("/login/")
async def user_login(user_login: UserLogin):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (user_login.username, user_login.password),
    )
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Login failed")
    
# -------------- Form Data --------------

@app.post("/enter_form_details/")
async def enter_form_details_and_create_room(form_data: FormData, user_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO form_data (user_id, destination, group_size, transportation_method) VALUES (?, ?, ?, ?)",
        (user_id, form_data.destination, form_data.group_size, form_data.transportation_method),
    )
    conn.commit()

    room_data = RoomCreate(user_id=user_id, room_name=form_data.destination, room_size=form_data.group_size)
    create_room(room_data) 

    cursor.close()
    return {"message": "Form data entered, and room created successfully"}


# -------------- Room creation--------------

def create_room(room_data: RoomCreate):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_rooms (room_name, room_size, admin_user_id) VALUES (?, ?, ?)",
        (room_data.room_name, room_data.room_size, room_data.user_id, room_data.room_id, room_data.room_type),
    )
    conn.commit()
    cursor.close()
    return {"message": "Room created successfully"}