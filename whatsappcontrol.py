import pywhatkit

rehber={
#########
}

def mesajGonder(isim, mesaj):
    isim = isim.lower()
    if isim in rehber:
        telefon = rehber[isim]
        pywhatkit.sendwhatmsg_instantly(telefon, mesaj, wait_time=10, tab_close=True)
        print(f"{isim} adlı kişiye mesaj gönderildi.")
    else:
        print(f"{isim} rehberde bulunamadı.")