import ollama

def generate_next_song_query(recent_history, current_mood_signal="neutral"):
    """
    Takes a summary of your music habits, passes them to your local 
    upgraded Qwen 3.5 9B model, and returns a direct search query string.
    """
    system_instruction = (
        "You are the autonomous routing core of an AI Music Player. Your job is to read "
        "the user's historical tracks, analyzing their current vibe, and output EXACTLY "
        "ONE search query string for the next track they should listen to. "
        "CRITICAL: Output absolutely NO conversational filler text, no punctuation markings, "
        "and no explanations. Output ONLY the plain search string (e.g., 'Linkin Park Numb Audio')."
    )
    
    user_prompt = f"""
    [Listening History Log]:
    {recent_history}
    
    [Current System Mood Metric]: {current_mood_signal}
    
    Based on the listening repetition pattern, tempo preference, and current mood state, 
    what exact track or sonic vibe should they listen to next? 
    Generate the plain text search string now.
    """
    
    print("🧠 Talking to local upgraded 9B model to analyze your mood vibe...")
    
    try:
        response = ollama.chat(
            model='qwen3.5:9b',
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"❌ Failed to communicate with Ollama: {e}")
        return None