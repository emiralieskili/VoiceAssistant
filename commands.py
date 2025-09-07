from speech import speak, listen
from datetime import datetime
import os
import spotifycontrol
import whatsappcontrol
import webcontrol
import intentrecognition

def process_command(command, sp, intent, intentEngine,awake=True):
    command = command.lower()
    #Basit sohbet
    if intent=="selamlama":
        speak("Merhaba! Size nasıl yardımcı olabilirim?")
        print("Merhaba! Size nasıl yardımcı olabilirim?")
    
    elif intent=="halHatır":
        speak("Ben bir sesli asistanım, duygularım yok ama size yardımcı olmak için buradayım. Siz nasılsınız?")
        print("Ben bir sesli asistanım, duygularım yok ama size yardımcı olmak için buradayım. Siz nasılsınız?")
    
    elif intent=="halHatırCevapOlumlu":
        speak("Bunu duyduğuma sevindim. Size nasıl yardımcı olabilirim?")
        print("Bunu duyduğuma sevindim. Size nasıl yardımcı olabilirim?")
    
    elif intent=="halHatırCevapOlumsuz":
        speak("Üzgünüm, umarım daha iyi hissedersiniz. Size nasıl yardımcı olabilirim?")
        print("Üzgünüm, umarım daha iyi hissedersiniz. Size nasıl yardımcı olabilirim?")
    
    #arama yapma
    elif intent=="googleArama":
        webcontrol.googleArama()
    
    elif intent=="youtubeArama":   
        webcontrol.youtubeArama()
    
    elif intent=="havaDurumu":
        webcontrol.weatherCondition()
    
    elif intent=="haberOku":
        webcontrol.haberOku()

    #spotify komutları
    elif intent=="müzikAç":
        speak("Hangi şarkıyı açmamı istersin?")
        print("Şarkı için dinleniyor...")
        song_name = listen()
        spotifycontrol.play_song(sp,song_name)
    
    elif intent=="müzikDeğiştir":
            speak("Hangi şarkıya geçmek istersin?")
            print("Şarkı için dinleniyor...")
            song_name = listen()
            spotifycontrol.play_song(sp,song_name)
            speak("Şarkı değiştirildi.")
            print("Şarkı değiştirildi.")

    elif intent=="müzikDurdur":
        sp.pause_playback()
        speak("Müzik durduruldu.")
        print("Müzik durduruldu.")
    
    elif intent=="playlistAç":
        spotifycontrol.play_playlist(sp)

    elif intent=="şarkıyaDevamEt":
        spotifycontrol.resume_playback(sp)
        speak("Müzik devam ediyor.")
        print("Müzik devam ediyor.")

    #whatsapp komutları
    elif intent=="mesajGönder":
        speak("Kime mesaj göndermek istersin?")
        print("Kişi için dinleniyor...")
        kisi = listen()
        speak("Ne göndereyim?")
        print("Mesaj için dinleniyor...")
        mesaj = listen()
        whatsappcontrol.mesajGonder(kisi, mesaj)

    # günlük komutlar
    elif intent=="saat":
        now = datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {now}")
        print(f"Saat: {now}")

    elif intent=="tarih":
        today = datetime.now().strftime("%d %B %Y")
        speak(f"Bugünün tarihi {today}")
        print(f"Bugünün tarihi: {today}")

    elif intent=="not":
        speak("Ne not almamı istersin?")
        print("Not almak için dinleniyor...")
        note = listen()
        if note:
            folder_path = os.getenv("SESLİ_ASİSTAN_NOTLARI_PATH")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            first_word = note.strip().split()[0]
            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"{first_word}_{date_str}.txt"
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(note + "\n")

            speak(f"Notunuz {filename} dosyasına kaydedildi.")
            print(f"Not kaydedildi: {file_path}")
        else:
            speak("Notu anlayamadım.")
            print("Notu anlayamadım.")

    #öğrenme
    elif intent == "komutEkle":
        speak("İntent adını söyleyin.")
        print("Intent adı için dinleniyor...")
        intent_name = listen()

        speak("Bu intent için bir komut cümlesi söyleyin.")
        print("Komut cümlesi için dinleniyor...")
        phrase = listen()

        if intent_name and phrase:
            intentrecognition.add_command(intent_name, phrase)
            speak("İntents.json dosyası güncellendi.")
            print("İntents.json dosyası güncellendi.")
        else:
            speak("Komut ekleme başarısız oldu, lütfen tekrar deneyin.")
            print("Komut ekleme başarısız oldu, lütfen tekrar deneyin.")

    #uyku ve çıkış
    elif intent=="uykuModu":
        speak("Uyku moduna geçiyorum. Uyandırmak için herhangi bir wakewordü söyleyin.")
        print("Uyku moduna geçildi.")
        awake = False
    
    elif intent=="çıkış":
        speak("Program kapatılıyor.")
        print("Program kapatılıyor.")
        exit()

    else:
        learned_intent = intentEngine.learn_new_phrase(command,learning_threshold=0.12)
        if learned_intent != "bilinmiyor":
            speak(f"Bunu öğrendim, '{learned_intent}' olarak kaydettim.")
            print(f"Öğrenilen intent: {learned_intent}")
            intent = learned_intent
            # burada istersen tekrar komutu çalıştırabilirsin
            # örneğin eğer learned_intent == "müzikAç" ise direkt şarkıyı aç
        else:
            speak(f"Anlamadım: {command}")
            print(f"Anlamadım: {command}")
    return awake