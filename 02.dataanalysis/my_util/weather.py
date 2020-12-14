import requests
from urllib.parse import urlparse
import pandas as pd

key_fd = open('openweatherkey.txt', mode='r')
oweather_key = key_fd.read(100)
key_fd.close()

lat = 37.5509655144007
lng = 126.849532173376
url =f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={oweather_key}&units=metric&lang=kr'

result = requests.get(urlparse(url).geturl()).json()

def get_weather():
    icon = result['weather'][0]['icon']
    desc = result['weather'][0]['description']
    temp = result['main']['temp']
    temp_min = result['main']['temp_min']
    temp_max = result['main']['temp_max']
    iconim = f'<img src= "http://openweathermap.org/img/w/{icon}.png" height="32">'
    return f'{iconim} {desc}, 온도: {temp},{temp_min}℃/{temp_max}℃'
