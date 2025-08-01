import pygame
from gtts import gTTS
import tempfile
import time
import speech_recognition as sr  # Dinleme fonksiyonların varsa burada tutabilirsin
import os

pygame.mixer.init()  # program başında bir kere çalışsın

def speak(text):
    tts = gTTS(text=text, lang='tr')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        file_path = fp.name

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    try:
        os.remove(file_path)
    except:
        pass
    
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinliyorum...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="tr-TR")
        print(f"Sen dedin ki: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Anlayamadım.")
        return ""
    except sr.RequestError:
        print("İnternet bağlantısı sorunlu.")
        return ""
