# music-mood-sync 🎵

An autonomous, offline AI music agent that indexes a local audio library, analyzes listening patterns, and automatically downloads and streams context-aware music using a local LLM and yt-dlp.

## 🛠️ Tech Stack & Architecture

- **Language:** Python
- **Database:** SQLite (Local Offline Memory)
- **AI Engine:** Local LLM via Ollama
- **Audio Pipeline:** yt-dlp & FFmpeg (320kbps HD Conversion)

## 📂 Project Structure

- `download_engine.py` — The free, high-definition downloading pipeline.
- `init_db.py` — Initializes the local SQLite memory engine.
- `.gitignore` — Strictly isolates and protects local audio storage from version control tracking.
