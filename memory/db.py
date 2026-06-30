import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secondbrain.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        goal_text TEXT NOT NULL,
        target_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        user_id TEXT NOT NULL,
        pref_key TEXT NOT NULL,
        pref_value TEXT NOT NULL,
        PRIMARY KEY (user_id, pref_key),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        query TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        confidence INTEGER,
        rationale TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        task_description TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills_progress (
        user_id TEXT NOT NULL,
        skill_name TEXT NOT NULL,
        progress_level TEXT NOT NULL,
        PRIMARY KEY (user_id, skill_name),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # Insert default user if not exists — NO preset preferences or goals.
    # Memory starts empty so the agent will ask the user for their context.
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES ('user_123', 'Default User')")
    
    conn.commit()
    conn.close()

