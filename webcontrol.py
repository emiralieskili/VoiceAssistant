import webbrowser
from speech import speak, listen
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
import wikipedia
load_dotenv()

env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

apiKeyWeather = os.getenv("WEATHER_API_KEY")  # OpenWeatherMap API key
apiKeyNews = os.getenv("NEWS_API_KEY")  # NewsAPI key

#Google arama
def googleArama():
    speak("Ne aramak istiyorsun?")
    while True:
        query = listen()
        if not query:
            speak("Anlayamadım, lütfen tekrar söyle.")
            continue
        if query.lower() in ["aramayı iptal et", "aramayı durdur", "iptal et"]:
            speak("Arama iptal edildi.")
            return
        
        # Google arama sayfasını aç
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        break

#YouTube arama
def youtubeArama():
    speak("Ne aramak istiyorsun?")
    while True:
        query = listen()
        if not query:
            speak("Anlayamadım, lütfen tekrar söyle.")
            continue
        if query.lower() in ["aramayı iptal et", "aramayı durdur", "iptal et"]:
            speak("Arama iptal edildi.")
            return
        
        # YouTube arama sayfasını aç
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        break

#Hava durumu
def weatherCondition():
    speak("Hava durumu bilgisi için lütfen bir şehir ismi söyleyin.")
    while True:
        sehir = listen()
        if not sehir:
            speak("Anlayamadım, lütfen tekrar söyle.")
            continue
        if sehir.lower() in ["aramayı iptal et", "aramayı durdur", "iptal et"]:
            speak("Hava durumu sorgulaması iptal edildi.")
            return
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={apiKeyWeather}&units=metric&lang=tr"
        response = requests.get(url)
        
        if response.status_code == 200:
            veri = response.json()
            sicaklik = veri["main"]["temp"]
            durum = veri["weather"][0]["description"]
            speak(f"{sehir} için hava durumu: {durum}, sıcaklık {sicaklik} derece.")
            break
        else:
            speak("Hata: Şehir bulunamadı veya hava durumu bilgisi alınamadı. Lütfen tekrar deneyin.")
            continue

# Haber okuma
def haberOku():
    while True:
        speak("Hangi kategoride haberleri okumak istersiniz? Spor, teknoloji, bilim, sağlık, eğlence, iş veya genel haberler?")
        kategoriler = ["sports", "technology", "science", "health", "entertainment", "business", "general"]
        kategori = listen()
        if not kategori:
            speak("Anlayamadım, lütfen tekrar söyle.")
            continue
        if kategori.lower() in ["iptal et", "durdur", "aramayı iptal et"]:
            speak("Haber okuma iptal edildi.")
            return
        kategori = kategori.lower()
        if kategori == "spor":
            kategori = "sports"
        elif kategori == "teknoloji":
            kategori = "technology"
        elif kategori == "bilim":
            kategori = "science"
        elif kategori == "sağlık":
            kategori = "health"
        elif kategori == "eğlence":
            kategori = "entertainment"
        elif kategori == "iş":
            kategori = "business"
        elif kategori == "genel":
            kategori = "general"
        if kategori not in kategoriler:
            speak("Geçersiz kategori, lütfen tekrar deneyin.")
            continue

        url = f"https://newsapi.org/v2/top-headlines?country=tr&category={kategori}&apiKey={apiKeyNews}"
        response = requests.get(url)

        if response.status_code == 200:
            haberler = response.json().get("articles", [])
            if not haberler:
                speak("Bugün haber bulunamadı.")
                return
            speak("İşte son haber başlıkları:")
            for haber in haberler[:5]:
                speak(haber["title"])
            break
        else:
            speak("Haberler alınırken hata oluştu.")
            break


# Wikipedia arama
def wikipediaAra():
    wikipedia.set_lang("tr")
    speak("Ne hakkında bilgi almak istersin?")
    while True:
        konu = listen()
        if not konu:
            speak("Anlayamadım, lütfen tekrar söyle.")
            continue
        if konu.lower() in ["aramayı iptal et", "aramayı durdur", "iptal et"]:
            speak("Arama iptal edildi.")
            return
    
        try:
            sonuc = wikipedia.summary(konu, sentences=2, auto_suggest=True, redirect=True)
            speak(sonuc)
            break
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"{konu} hakkında çok fazla sonuç var. Lütfen daha spesifik bir konu belirt.")
        except wikipedia.exceptions.PageError:
            speak(f"{konu} hakkında bilgi bulunamadı.")
        except Exception as e:
            speak("Bir hata oluştu, lütfen tekrar deneyin.")
            print(f"Hata: {e}")
            break