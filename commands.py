from speech import speak, listen
from datetime import datetime
import os
import spotifycontrol
import whatsappcontrol
import webcontrol

def process_command(command, sp, awake=True):
    command = command.lower()

    if "nasılsın" in command:
        speak("İyiyim, teşekkürler. Sen nasılsın?")
    
    #arama yapma
    elif "google'da ara" in command:
        webcontrol.googleArama()
    
    elif "youtube'da ara" in command:   
        webcontrol.youtubeArama()
    
    elif "hava durumu" in command:
        webcontrol.weatherCondition()
    
    elif "haber oku" in command or "haberler" in command:
        webcontrol.haberleri_oku()

    #spotify komutları
    elif "müzik aç" in command or "şarkı aç" in command:
        speak("Hangi şarkıyı açmamı istersin?")
        song_name = listen()
        acikmi=True
        spotifycontrol.play_song(song_name, sp)
    
    elif "müzik değiştir" in command or "şarkı değiştir" in command:
        if acikmi:
            speak("Hangi şarkıya geçmek istersin?")
            song_name = listen()
            spotifycontrol.play_song(song_name, sp)
            speak("Şarkı değiştirildi.")
        else:
            speak("Önce müzik açmalısın.")

    elif "şarkı durdur" in command or "müzik durdur" in command:
        sp.pause_playback()
        speak("Müzik durduruldu.")
        acikmi=False
    
    elif "çalma listesini aç" in command or "playlisti aç" in command:
        spotifycontrol.play_playlist(sp)

    elif "şarkıya devam et" in command or "müziğe devam et" in command:
        spotifycontrol.resume_playback(sp)

    #whatsapp komutları
    elif "mesaj gönder" in command or "mesaj at" in command:
        speak("Kime mesaj göndermek istersin?")
        kisi = listen()
        speak("Ne göndereyim?")
        mesaj = listen()
        whatsappcontrol.mesajGonder(kisi, mesaj)

    # günlük kullanılabilecek komutlar
    elif "saat kaç" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {now}")

    elif "bugünün tarihi ne" in command:
        today = datetime.now().strftime("%d %B %Y")
        speak(f"Bugünün tarihi {today}")

    elif "not al" in command:
        speak("Ne not almamı istersin?")
        note = listen()
        if note:
            folder_path = r"----" # Notların kaydedileceği klasör yolu
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            first_word = note.strip().split()[0]
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"{first_word}_{date_str}.txt"
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(note + "\n")

            speak(f"Notunuz {filename} dosyasına kaydedildi.")
        else:
            speak("Notu anlayamadım.")

    #uyku ve çıkış
    elif "kapat" in command or "çıkış" in command:
        speak("Program kapatılıyor.")
        exit()

    elif "uyku moduna geç" in command:
        speak("Uyku moduna geçiyorum. Uyandırmak için herhangi bir wakeword söyleyin.")
        awake = False

    else:
        speak(f"Anlamadım: {command}")

    return awake