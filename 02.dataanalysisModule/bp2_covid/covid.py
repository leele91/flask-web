from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import timedelta
import os, folium, json
import pandas as pd
from my_util.weather import get_weather # 네비바 날짜 모듈

covid_bp = Blueprint('covid_bp', __name__)

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

# 코로나 확진자 현황 
@covid_bp.route('/daily')
def daily():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    