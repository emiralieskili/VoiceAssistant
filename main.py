from speech import speak, listen
import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pathlib import Path
import os
from intentrecognition import IntentRecognition

# .env dosyasını yükle
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Spotipy yetkilendirme
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-modify-playback-state user-read-playback-state playlist-read-private"
))  

# Uyandırma kelimeleri
wakeWords = ["bilgisayar"]

def main():
    awake = False
    intentEngine = IntentRecognition()  # intent motoru

    while True:
        command = listen()

        if not command:
            continue

        command = command.lower()

        if not awake:
            if any(word in command.lower() for word in wakeWords):
                speak("Dinliyorum.")
                awake = True
            else:
                continue
        else:
            # intent burada bulunuyor
            intent = intentEngine.get_intent(command)
            awake = commands.process_command(command, sp, intent,intentEngine, awake)

if __name__ == "__main__":
    main()
