from speech import speak, listen
import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotipy yetkilendirme
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    ######
))

wakeWords=["bilgisayar","asistan","sesli asistan"]

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
