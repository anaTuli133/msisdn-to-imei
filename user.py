import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
# DB_PATH = r"D:\Anamika\MyAPI\users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create users table if not exists"""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str):
    """Add a new 3rd party user"""
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        print(f"✅ User '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"❌ User '{username}' already exists.")
    finally:
        conn.close()

def verify_user(username: str, password: str) -> bool:
    """Check username + password"""
    conn = get_db()
    row = conn.execute(
        "SELECT password, is_active FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if not row:
        return False
    if not row["is_active"]:
        return False
    return row["password"] == hash_password(password)

def list_users():
    conn = get_db()
    rows = conn.execute("SELECT id, username, is_active, created_at FROM users").fetchall()
    conn.close()
    return rows

def deactivate_user(username: str):
    conn = get_db()
    conn.execute("UPDATE users SET is_active = 0 WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# Auto-initialize DB on import
init_db()