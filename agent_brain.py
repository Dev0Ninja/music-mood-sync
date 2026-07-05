import os
from google import genai
from google.genai import types

# Initialize the Gemini Client
# It automatically looks for the GEMINI_API_KEY environment variable.
client = genai.Client()

def generate_next_song_query(history_context="", current_mood_signal=""):
    """
    Connects to Google AI Studio to analyze your mood signal and history logs,
    matching the exact parameter naming expected by your main.py controller.
    """
    system_instruction = (
        "You are the central nervous system brain of an AI Music Agent. Your only job is to analyze "
        "the user's request and their past listening patterns, then suggest the ONE exact track title "
        "and artist they should listen to next. "
        "CRITICAL RULE: You must return ONLY the plain text search string (e.g., 'Linkin Park Numb Audio'). "
        "Do not include quotes, conversational text, pleasantries, or formatting headers."
    )
    
    # Construct the context prompt using the variables passed from main.py
    if current_mood_signal:
        prompt = f"The user manually requested this vibe/mood: '{current_mood_signal}'.\n"
    else:
        prompt = "The user left the vibe empty. Predict their mood entirely from history.\n"
        
    prompt += f"Recent Historical Data (Song, Action, Vibe):\n{history_context}\n"
    prompt += "What is the single best track they need to hear right now? Output search query text only:"

    try:
        # Call the cloud Gemini 3.5 Flash model
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        
        # Clean up the output string
        search_query = response.text.strip().replace('"', '').replace("'", "")
        return search_query
        
    except Exception as e:
        print(f"❌ Cloud AI Brain Error: {e}")
        return None

if __name__ == "__main__":
    # This block only runs if you play agent_brain.py directly to test your API connection
    print("🧠 Testing Cloud Gemini Brain Structure...")
    sample_history = "1. Mango Flame | Played | neutral"
    test_result = generate_next_song_query(history_context=sample_history, current_mood_signal="3am coding session")
    print(f"🤖 AI Generated Search String: '{test_result}'")