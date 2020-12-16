from flask import Flask, render_template, session, request
from bp5_stock.stock import stock_bp
from bp1_seoul.seoul import seoul_bp
import os, folium, json, logging
from logging.config import dictConfig
import pandas as pd
import pandas_datareader as pdr
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from my_util.weather import get_weather

# 한글폰트 사용
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)

app = Flask(__name__)
app.secret_key = 'qwert12345'
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(seoul_bp, url_prefix='/seoul')

# 로그인 
with open('./logging.json', 'r') as file:
    config = json.load(file)
dictConfig(config)
app.logger


def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 'se':0, 'co':0, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    return render_template('index.html', menu=menu, weather=get_weather_main())



if __name__ == '__main__':
    app.run(debug=True)