import os
import sqlite3
from init_db import register_downloaded_track, log_user_feedback 
from download_engine import download_hd_track
from agent_brain import generate_next_song_query

def get_recent_history_from_db():
    """
    Queries the offline SQLite database to fetch the last 5 tracking logs.
    """
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT t.title, h.action, h.vibe_tag 
            FROM history h
            JOIN tracks t ON h.track_id = t.id
            ORDER BY h.timestamp DESC 
            LIMIT 5
        ''')
        rows = cursor.fetchall()
        if not rows:
            return "No history found yet. Brand new profile."
        history_lines = []
        for i, row in enumerate(rows, 1):
            history_lines.append(f"{i}. Song: '{row[0]}' | Action: {row[1]} | Vibe context: {row[2]}")
        return "\n".join(history_lines)
    except sqlite3.OperationalError as e:
        print(f"⚠️ Database read error: {e}.")
        return "Database not initialized."
    finally:
        conn.close()

def find_track_locally(user_input):
    """
    Performs a local lookup to see if the track exists in your folder cache.
    """
    conn = sqlite3.connect("agent_memory.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT title, file_path FROM tracks WHERE title LIKE ? AND status = 'active'", (f"%{user_input}%",))
        result = cursor.fetchone()
        return result
    except Exception:
        return None
    finally:
        conn.close()

def run_interactive_music_agent():
    print("\n🤖 AI MUSIC AGENT ONLINE...")
    
    # 1. Gather true history context from your SQLite files
    real_history_context = get_recent_history_from_db()
    
    # 2. Extract the literal last song heard AND what you did with it (played vs skipped)
    temp_conn = sqlite3.connect("agent_memory.db")
    cursor = temp_conn.cursor()
    
    last_song_name = "None"
    last_action = "none"
    last_liked_song = "None"
    
    try:
        # Get the absolute last interaction
        cursor.execute("""
            SELECT t.title, h.action 
            FROM history h 
            JOIN tracks t ON h.track_id = t.id 
            ORDER BY h.timestamp DESC 
            LIMIT 1
        """)
        last_row = cursor.fetchone()
        if last_row:
            last_song_name, last_action = last_row[0], last_row[1]
            
        # Get the last song that was successfully PLAYED (Liked)
        cursor.execute("""
            SELECT t.title 
            FROM history h 
            JOIN tracks t ON h.track_id = t.id 
            WHERE h.action = 'played'
            ORDER BY h.timestamp DESC 
            LIMIT 1
        """)
        liked_row = cursor.fetchone()
        if liked_row:
            last_liked_song = liked_row[0]
            
    except Exception as e:
        print(f"⚠️ Error reading memory strings: {e}")
    finally:
        temp_conn.close()
    
    # Visual system logging updates
    print(f"📻 Last track encountered: '{last_song_name}' [Status: {last_action.upper()}]")
    if last_action == "skipped":
        print(f"⭐ Last anchoring LIKED song: '{last_liked_song}'")
    
    # 3. Prompt user for custom instruction
    user_vibe_check = input("🎵 Your Vibe Request (Or leave empty/press Enter to follow memory queue): ").strip()
    
    # Cache verification routing logic
    if user_vibe_check:
        local_hit = find_track_locally(user_vibe_check)
        if local_hit:
            print(f"⚡ [LOCAL CACHE HIT] '{local_hit[0]}' found locally at: {local_hit[1]}")
            print("▶️ Simulating local track playback...")
            return

    # Handle fallback context based on reinforcement rules
    if not user_vibe_check:
        if last_action == "skipped":
            print(f"🧠 Negative feedback detected! Pivoting away from '{last_song_name}'...")
            mood_signal = (
                f"CRITICAL: The user just SKIPPED and disliked the track '{last_song_name}'. Do NOT suggest anything "
                f"similar to that song's sound, artist, or energy. Instead, pivot completely and pick a song that "
                f"matches the energy flow of their last LIKED song: '{last_liked_song}'."
            )
        else:
            print(f"🧠 Positive flow confirmed. Continuing queue based on your last track: '{last_song_name}'...")
            mood_signal = f"Predict next track directly continuing the energy flow of my last song: '{last_song_name}'"
    else:
        mood_signal = user_vibe_check

    print("☁️ Consulting Cloud Gemini Brain for your custom suggestion...")
    predicted_search_query = generate_next_song_query(history_context=real_history_context, current_mood_signal=mood_signal)
    
    if not predicted_search_query:
        print("❌ Could not generate next song recommendation.")
        return
        
    print(f"🎯 Cloud AI recommends searching for: '{predicted_search_query}'")
    
    # Check if AI's generated song name happens to be in your local drive cache database
    local_hit = find_track_locally(predicted_search_query)
    if local_hit:
        print(f"⚡ [LOCAL CACHE HIT] Cloud suggested a track you already own: '{local_hit[0]}'")
        print(f"📁 Local Path: {local_hit[1]}")
        return
        
    # Trigger your working downloader module stream
    print("📥 Initializing cloud download bridge...")
    downloaded_file_path = download_hd_track(predicted_search_query)
    
    if downloaded_file_path:
        inferred_title = os.path.basename(downloaded_file_path).replace(".mp3", "")
        
        # Write to SQLite memory blocks
        track_id = register_downloaded_track(inferred_title, downloaded_file_path)
        
        print(f"\n🎧 Finished downloading: '{inferred_title}'")
        print("1. Loved it / Listened completely")
        print("2. Skipped it / Move to next track")
        
        try:
            feedback_choice = input("Select an action option (1 or 2): ").strip()
            action_tag = "played" if feedback_choice == "1" else "skipped"
            
            # Log exact feedback interaction into your database history grid
            log_user_feedback(track_id, action=action_tag, vibe_tag=mood_signal)
        except Exception as e:
            print(f"⚠️ Feedback processing skipped: {e}")
            
if __name__ == "__main__":
    run_interactive_music_agent()