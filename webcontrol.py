import webbrowser
from speech import speak, listen
import requests

apiKeyWeather = ""  # OpenWeatherMap API key
apiKeyNews = ""  # NewsAPI key

def googleArama():
    speak("Ne aramak istiyorsun?")
    query = listen()
    if not query:
        speak("Anlayamadım, lütfen tekrar söyle.")
        return
    
    # Google arama sayfasını aç
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def youtubeArama():
    speak("Ne aramak istiyorsun?")
    query = listen()
    if not query:
        speak("Anlayamadım, lütfen tekrar söyle.")
        return
    
    # YouTube arama sayfasını aç
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)

def weatherCondition():
    speak("Hava durumu bilgisi için lütfen bir şehir ismi söyle.")
    sehir = listen()
    if not sehir:
        speak("Anlayamadım, lütfen tekrar söyle.")
        return
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={apiKeyWeather}&units=metric&lang=tr"
    response = requests.get(url)
    
    if response.status_code == 200:
        veri = response.json()
        sicaklik = veri["main"]["temp"]
        durum = veri["weather"][0]["description"]
        speak(f"{sehir} için hava durumu: {durum}, sıcaklık {sicaklik} derece.")
    else:
        speak("Hava durumu bilgisi alınamadı.")

def haberleri_oku():
    url = f"https://newsapi.org/v2/top-headlines?country=tr&apiKey={apiKeyNews}"
    response = requests.get(url)
    
    if response.status_code == 200:
        haberler = response.json().get("articles", [])
        if not haberler:
            speak("Bugün haber bulunamadı.")
            return
        speak("İşte son haber başlıkları:")
        for haber in haberler[:5]:  # İlk 5 haberi oku
            speak(haber["title"])
    else:
        speak("Haberler alınırken hata oluştu.")