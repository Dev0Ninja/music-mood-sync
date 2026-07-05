import os
from agent_brain import generate_next_song_query
from download_engine import download_hd_track

def run_autonomous_music_agent_loop(mood_input):
    print("🤖 AI MUSIC AGENT PIPELINE OVERHEAD ONLINE...")
    print(f"🎭 Current Vibe Target: '{mood_input}'")
    print("-" * 50)
    
    # Simulating what your future database history log data will feed into the brain
    sample_history_context = (
        "- Played: Mango Flame (Vibe: Ambient chill electronic)\n"
        "- Played: Lofi Hip Hop study beats track\n"
        "- Skipped: High-tempo EDM workout song (Skipped in 5 seconds)"
    )
    
    # 1. Ask the 9B model to invent the next track target phrase
    predicted_search_query = generate_next_song_query(sample_history_context, current_mood_signal=mood_input)
    
    if not predicted_search_query:
        print("❌ Agent Brain failed to yield a target direction.")
        return
        
    print(f"🔮 Local LLM calculated query: '{predicted_search_query}'")
    print("-" * 50)
    
    # 2. Feed that string variable straight to the browser authenticated downloader script
    print("📥 Commencing autonomous video capture stream...")
    saved_file_path = download_hd_track(predicted_search_query)
    
    if saved_file_path:
        print("\n🎉 SUCCESSFUL COMPLETE AGENT CYCLE!")
        print(f"🎵 Media track compiled safely on disc: {saved_file_path}")
    else:
        print("\n❌ Pipeline stalled during media translation extraction.")

if __name__ == "__main__":
    # Change this phrase text to see how the model dynamically pivots its search outputs!
    user_vibe_check = "late night dark coding session"
    run_autonomous_music_agent_loop(user_vibe_check)