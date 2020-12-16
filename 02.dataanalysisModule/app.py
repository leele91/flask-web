from flask import Flask, render_template, session, request
from bp5_stock.stock import stock_bp
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

@app.route('/park', methods=['GET', 'POST'])
def park():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':1, 'co':0, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    park_gu = pd.read_csv('./static/data/park_gu.csv')
    park_gu.set_index('지역', inplace=True)
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in park_new.index:
            folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                radius=int(park_new['size'][i]),
                                tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                color='#3186cc', fill_color='#3186cc').add_to(map)
        html_file = os.path.join(app.root_path, 'static/img/park.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)
        return render_template('park.html', menu=menu, weather=get_weather_main(),
                                park_list=list(park_new['공원명']), gu_list=list(park_gu.index),
                                mtime=mtime)
    else:
        gubun = request.form['gubun']
        if gubun == 'park':
            park_name = request.form['name']
            df = park_new[park_new['공원명'] == park_name].reset_index()
            park_result = {'name':park_name, 'addr':df['공원주소'][0], 
                            'area':int(df.area[0]), 'desc':df['공원개요'][0]}
            map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
            for i in park_new.index:
                folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                    radius=int(park_new['size'][i]),
                                    tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            folium.CircleMarker([df.lat[0], df.lng[0]], radius=int(df['size'][0]),
                                    tooltip=f"{df['공원명'][0]}({int(df.area[0])}㎡)",
                                    color='crimson', fill_color='crimson').add_to(map)
            html_file = os.path.join(app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('park_res.html', menu=menu, weather=get_weather_main(),
                                    park_result=park_result, mtime=mtime)
        else:
            gu_name = request.form['gu']
            df = park_gu[park_gu.index == gu_name].reset_index()
            park_result = {'gu':df['지역'][0], 
                            'area':int(df['공원면적'][0]), 'm_area':int(park_gu['공원면적'].mean()),
                            'count':df['공원수'][0], 'm_count':round(park_gu['공원수'].mean(),1),
                            'area_ratio':round(df['공원면적비율'][0],2), 'm_area_ratio':round(park_gu['공원면적비율'].mean(),2),
                            'per_person':round(df['인당공원면적'][0],2), 'm_per_person':round(park_gu['인당공원면적'].mean(),2)}
            df = park_new[park_new['지역'] == gu_name].reset_index()
            map = folium.Map(location=[df.lat.mean(), df.lng.mean()], zoom_start=13)
            for i in df.index:
                folium.CircleMarker([df.lat[i], df.lng[i]], 
                                    radius=int(df['size'][i])*3,
                                    tooltip=f"{df['공원명'][i]}({int(df.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            html_file = os.path.join(app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('park_res2.html', menu=menu, weather=get_weather_main(),
                                    park_result=park_result, mtime=mtime)

@app.route('/park_gu/<option>')
def park_gu(option):
    menu = {'ho':0, 'da':1, 'ml':0, 'se':1, 'co':0, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    park_gu = pd.read_csv('./static/data/park_gu.csv')
    park_gu.set_index('지역', inplace=True)
    geo_str = json.load(open('./static/data/skorea_municipalities_geo_simple.json',
                        encoding='utf8'))
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    if option == 'area':
        map.choropleth(geo_data = geo_str,
                        data = park_gu['공원면적'],
                        columns = [park_gu.index, park_gu['공원면적']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
    elif option == 'count':
        map.choropleth(geo_data = geo_str,
                        data = park_gu['공원수'],
                        columns = [park_gu.index, park_gu['공원수']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
    elif option == 'area_ratio':
        map.choropleth(geo_data = geo_str,
                        data = park_gu['공원면적비율'],
                        columns = [park_gu.index, park_gu['공원면적비율']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')
    elif option == 'per_person':
        map.choropleth(geo_data = geo_str,
                        data = park_gu['인당공원면적'],
                        columns = [park_gu.index, park_gu['인당공원면적']],
                        fill_color = 'PuRd',
                        key_on = 'feature.id')

    for i in park_new.index:
        folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                        radius=int(park_new['size'][i]),
                        tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                        color='green', fill_color='green').add_to(map)
    html_file = os.path.join(app.root_path, 'static/img/park_gu.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    option_dict = {'area':'공원면적', 'count':'공원수', 'area_ratio':'공원면적 비율', 'per_person':'인당 공원면적'}
    return render_template('park_gu.html', menu=menu, weather=get_weather_main(),
                            option=option, option_dict=option_dict, mtime=mtime)



if __name__ == '__main__':
    app.run(debug=True)