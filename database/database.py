"""
database.py
------------
All raw SQLite access for NutriVoice lives here. No UI code should ever
open a database connection directly — everything goes through the
functions in this file so the storage layer can be swapped later
(e.g. for a real server database) without touching the Streamlit pages.
"""

import sqlite3
import os
from datetime import datetime

# The .db file is created automatically the first time the app runs.
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nutrivoice.db")


def get_connection():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the users table if it does not already exist. Safe to call every app run."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            bmi REAL,
            user_type TEXT NOT NULL,
            pregnancy_month INTEGER,
            child_age INTEGER,
            child_gender TEXT,
            food_preference TEXT,
            dietary_preference TEXT,
            preferred_language TEXT,
            food_allergies TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def create_user(data: dict) -> int:
    """Insert a new profile. Returns the new row's id."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")
    cursor.execute(
        """
        INSERT INTO users (
            full_name, age, gender, phone, email, height, weight, bmi,
            user_type, pregnancy_month, child_age, child_gender,
            food_preference, dietary_preference, preferred_language,
            food_allergies, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("full_name"),
            data.get("age"),
            data.get("gender"),
            data.get("phone"),
            data.get("email"),
            data.get("height"),
            data.get("weight"),
            data.get("bmi"),
            data.get("user_type"),
            data.get("pregnancy_month"),
            data.get("child_age"),
            data.get("child_gender"),
            data.get("food_preference"),
            data.get("dietary_preference"),
            data.get("preferred_language"),
            data.get("food_allergies"),
            now,
            now,
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_user(user_id: int, data: dict) -> None:
    """Update an existing profile by id."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat(timespec="seconds")
    cursor.execute(
        """
        UPDATE users SET
            full_name = ?, age = ?, gender = ?, phone = ?, email = ?,
            height = ?, weight = ?, bmi = ?, user_type = ?,
            pregnancy_month = ?, child_age = ?, child_gender = ?,
            food_preference = ?, dietary_preference = ?,
            preferred_language = ?, food_allergies = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            data.get("full_name"),
            data.get("age"),
            data.get("gender"),
            data.get("phone"),
            data.get("email"),
            data.get("height"),
            data.get("weight"),
            data.get("bmi"),
            data.get("user_type"),
            data.get("pregnancy_month"),
            data.get("child_age"),
            data.get("child_gender"),
            data.get("food_preference"),
            data.get("dietary_preference"),
            data.get("preferred_language"),
            data.get("food_allergies"),
            now,
            user_id,
        ),
    )
    conn.commit()
    conn.close()


def get_user(user_id: int):
    """Fetch a single profile by id. Returns a dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_latest_user():
    """
    Fetch the most recently created/updated profile.
    Used so the app can 'remember' the demo profile between reruns
    without a full login system (this is a single-profile prototype).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_user(user_id: int) -> None:
    """Delete a profile by id (used only for testing/reset, not exposed in the UI)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
