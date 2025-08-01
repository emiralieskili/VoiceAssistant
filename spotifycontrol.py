from speech import speak, listen
import spotipy
import os
import time

def spotifyAc():
    import psutil
    spotify_yolu = r"--------"  # Spotify uygulamasının tam yolu
    
    spotify_acik = any("Spotify.exe" in p.name() for p in psutil.process_iter())
    if not spotify_acik:
        os.startfile(spotify_yolu)
        time.sleep(5)  # Spotify açılması için 5 saniye bekle



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
    results = sp.current_user_playlists()
    playlists = results['items']

    if not playlists:
        speak("Kitaplığında çalma listesi yok.")
        return

    print("Çalma listelerin:")


    speak("Hangi çalma listesini açmamı istersin?")
    choice = listen()
    if not choice:
        speak("Anlayamadım.")
        return

    choice = choice.lower()
    for playlist in playlists:
        if choice in playlist['name'].lower():
            sp.start_playback(context_uri=playlist['uri'])
            speak(f"{playlist['name']} çalıyor.")
            return

    speak("Seçtiğin çalma listesi bulunamadı.")


def play_song(song_name, sp):  # sp eklendi
    spotifyAc()

    results = sp.search(q=song_name, limit=1, type="track")
    tracks = results.get("tracks", {}).get("items", [])

    if not tracks:
        speak("Şarkı bulunamadı.")
        return

    track_uri = tracks[0]["uri"]
    devices = sp.devices()

    if not devices["devices"]:
        speak("Aktif Spotify cihazı yok.")
        return

    device_id = devices["devices"][0]["id"]
    sp.start_playback(device_id=device_id, uris=[track_uri])
