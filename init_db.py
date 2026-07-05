import sqlite3

def initialize_database():
    # Automatically creates the local database file in your folder
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()
    
    # 1. Tracks Table: Stores local song metadata and paths
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        file_path TEXT UNIQUE,
        status TEXT DEFAULT 'active' -- 'active', 'archived', or 'disliked'
    )
    """)
    
    # 2. History Table: Logs your listening patterns, skips, and choices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        action TEXT, -- Logs actions like 'played', 'skipped', or 'disliked'
        FOREIGN KEY (track_id) REFERENCES tracks(id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("🧠 AI Agent Memory Database successfully initialized!")

if __name__ == "__main__":
    initialize_database()