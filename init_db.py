import sqlite3

def initialize_database():
    """Automatically creates the local database file and its foundational structure."""
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
        vibe_tag TEXT DEFAULT 'neutral',
        FOREIGN KEY (track_id) REFERENCES tracks(id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("🧠 AI Agent Memory Database successfully initialized!")

def register_downloaded_track(title, file_path):
    """Saves a successfully downloaded song's path into our tracking table."""
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()
    try:
        # Adjusted table name to match 'tracks'
        cursor.execute(
            "INSERT OR IGNORE INTO tracks (title, file_path) VALUES (?, ?)", 
            (title, file_path)
        )
        conn.commit()
        
        # Fetch the ID of the song we just logged
        cursor.execute("SELECT id FROM tracks WHERE file_path = ?", (file_path,))
        track_id = cursor.fetchone()[0]
        return track_id
    except Exception as e:
        print(f"Database write error: {e}")
        return None
    finally:
        conn.close()

def log_user_feedback(track_id, action, vibe_tag="neutral"):
    """Logs whether you skipped, completed, or disliked a song."""
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()
    try:
        # Adjusted table name to match 'history' and matching column fields
        cursor.execute(
            "INSERT INTO history (track_id, action, vibe_tag) VALUES (?, ?, ?)",
            (track_id, action, vibe_tag)
        )
        conn.commit()
        print(f"💾 Logged feedback to database: Track #{track_id} was marked as '{action.upper()}'")
    except Exception as e:
        print(f"Database log error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()