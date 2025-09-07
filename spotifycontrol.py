from speech import speak, listen
import spotipy
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import psutil
from rapidfuzz import fuzz  # fuzzy matching için

load_dotenv()
env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

def normalize(text):
    replacements = {
        'ç':'c', 'Ç':'C',
        'ş':'s', 'Ş':'S',
        'ğ':'g', 'Ğ':'G',
        'ü':'u', 'Ü':'U',
        'ö':'o', 'Ö':'O',
        'ı':'i', 'İ':'I',
        '’':"'", '"':''
    }
    for k,v in replacements.items():
        text = text.replace(k,v)
    return text.lower()

def spotifyAc():
    spotify_yolu = os.getenv("SPOTIFY_PATH")
    if not spotify_yolu:
        speak("Spotify yolu .env dosyasında tanımlı değil.")
        return

    spotify_acik = any("Spotify.exe" in p.name() for p in psutil.process_iter())
    if not spotify_acik:
        os.startfile(spotify_yolu)
        time.sleep(5)

def resume_playback(sp):
    devices = sp.devices()
    if not devices['devices']:
        speak("Spotify'da açık bir cihaz yok. Lütfen Spotify uygulamasını aç.")
        return
    try:
        sp.start_playback()
        speak("Şarkıya devam ediliyor.")
    except spotipy.exceptions.SpotifyException as e:
        print(e)
        speak("Şarkıya devam edilemedi.")

def play_playlist(sp):
    spotifyAc()
    while True:
        results = sp.current_user_playlists()
        playlists = results.get('items', [])
        if not playlists:
            speak("Kitaplığında çalma listesi yok.")
            return

        speak("Hangi çalma listesini açmamı istersin?")
        choice = listen()
        if not choice:
            speak("Anlayamadım. Lütfen tekrar söyle.")
            continue

        if choice.lower() in ["iptal", "çık", "vazgeç"]:
            speak("İptal edildi.")
            return

        found = False
        for playlist in playlists:
            if choice.lower() in playlist['name'].lower():
                sp.start_playback(context_uri=playlist['uri'])
                speak(f"{playlist['name']} çalıyor.")
                found = True
                break

        if found:
            return
        else:
            speak("Seçtiğin çalma listesi bulunamadı. Tekrar söyle.")

def play_song(sp, song_name=None):
    spotifyAc()

    while True:
        if not song_name:
            speak("Hangi şarkıyı açmamı istersin?")
            song_name = listen()

        if not song_name:
            speak("Anlayamadım. Lütfen tekrar söyle.")
            continue

        if song_name.lower() in ["iptal", "çık", "vazgeç"]:
            speak("İptal edildi.")
            return

        song_name_norm = normalize(song_name)
        results = sp.search(q=f"track:{song_name_norm}", type="track", limit=5)
        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            speak("Şarkı bulunamadı. Tekrar söyle.")
            song_name = None
            continue

        # Fuzzy matching ile en yakın şarkıyı bul
        best_track = None
        highest_score = 0
        for track in tracks:
            track_name_norm = normalize(track['name'])
            score = fuzz.ratio(track_name_norm, song_name_norm)
            if score > highest_score:
                highest_score = score
                best_track = track

        if not best_track:
            speak("Şarkı bulunamadı. Tekrar söyle.")
            song_name = None
            continue

        devices = sp.devices()
        if not devices['devices']:
            speak("Aktif Spotify cihazı yok.")
            return

        device_id = devices['devices'][0]['id']
        sp.start_playback(device_id=device_id, uris=[best_track['uri']])
        speak(f"{best_track['name']} çalıyor.")
        return
