from speech import speak, listen
import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

# Spotipy yetkilendirme
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-modify-playback-state user-read-playback-state playlist-read-private"
))  

wakeWords=["kaya","bilgisayar","asistan","sesli asistan"]

def main():
    awake = False

    while True:
        command = listen()

        if not command:
            continue

        if not awake:
            if any(wakeWords in command for wakeWords in wakeWords):
                speak("Dinliyorum.")
                awake = True
            else:
                continue
        else:
            awake = commands.process_command(command, sp, awake)  # sp parametresi eklendi

if __name__ == "__main__":
    main()
