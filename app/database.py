import sqlite3

DATABASE_NAME = "finmark.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_user(name, email, password_hash, role, department):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role, department)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, password_hash, role, department))

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    return user_id


def find_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    connection.close()

    return dict(user) if user else None