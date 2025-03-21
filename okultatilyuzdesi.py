import requests
import datetime


API_KEY = input('lütfen API keyinizi giriniz: ')

# Hava durumu bilgilerini alacak fonksiyon
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return weather_description, temperature
    else:
        return None, None

# Okul tatil olma ihtimalini hesaplayan fonksiyon
def school_holiday_chance(weather_description, temperature):
    chance = 0

    # Eğer kar yağışı varsa tatil olma olasılığı yüksek
    if 'snow' in weather_description:
        chance += 40  # Kar yağışı = %40
    # Hava çok soğuksa, tatil olma ihtimali artabilir
    if temperature <= 0:
        chance += 20  # Soğuk hava = %20
    # Eğer fırtına varsa, tatil olma olasılığı artar
    elif 'storm' in weather_description:
        chance += 30  # Fırtına = %30

    # Hafta sonu olduğu için tatil, ihtimal 100%
    today = datetime.datetime.today().weekday()
    if today == 5 or today == 6:  # 5: Cumartesi, 6: Pazar
        chance = 100

    # Basit bir resmi tatil kontrolü (örneğin, yılbaşı, 23 Nisan gibi)
    today_date = datetime.datetime.today()
    holidays = [
        (1, 1),  # 1 Ocak (Yılbaşı)
        (4, 23), # 23 Nisan
        (5, 19), # 19 Mayıs
        (8, 30), # 30 Ağustos
        (10, 29), # 29 Ekim
    ]
    
    if (today_date.month, today_date.day) in holidays:
        chance = 100  # Eğer bugün resmi tatilse, tatil olma ihtimali %100

    # 0-100 arası tatil olma ihtimali
    return chance

# Kullanıcıdan şehir ismini al
city = input("Okulların tatil olup olmadığını öğrenmek için bir şehir girin: ")

# Hava durumu verilerini al
weather_description, temperature = get_weather(city)

if weather_description and temperature is not None:
    print(f"\n{city} Şehri İçin Hava Durumu:")
    print(f"Hava Durumu: {weather_description}")
    print(f"Sıcaklık: {temperature}°C")

    # Tatil olma ihtimalini hesapla
    holiday_chance = school_holiday_chance(weather_description, temperature)
    print(f"Okulların tatil olma ihtimali: %{holiday_chance}")
else:
    print("Hata: Şehir bulunamadı veya API isteği başarısız oldu.")
