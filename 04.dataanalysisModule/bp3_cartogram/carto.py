from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import timedelta
import os, folium, json
import pandas as pd
from my_util.weather import get_weather
import my_util.drawKorea as dk

carto_bp = Blueprint('carto_bp', __name__)

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

# 인구소멸지수
@carto_bp.route('/pop/<option>')
def population(option):
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':0, 'cg':1, 'cr':0, 'st':0, 'wc':0}
    df_pop = pd.read_csv('./static/data/population.csv')
    column_dict = {'extinction': '소멸위기지역', 'g_extinction':'소멸비율'}
    color_dict = {'extinction':'Blues', 'g_extinction': 'Greens'}

    img_file = os.path.join(current_app.root_path, 'static/img/population.png') # 파일이름
    dk.drawKorea(column_dict[option], df_pop, color_dict[option], img_file) # 소멸위기지역, df, 컬러, 이미지파일 전달
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('cartogram/population.html', menu=menu, weather=get_weather(), 
                                option=option, column_dict=column_dict, mtime=mtime)

# 커피지수
@carto_bp.route('/coffee', methods=['GET', 'POST'])
def coffee():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':0, 'cg':1, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        return render_template('cartogram/coffee.html', menu=menu, weather=get_weather_main())
    else:
        item = request.form['item'] # 파일 저장
        f = request.files['csv']
        #filename = os.path.join(current_app.root_path, 'static/upload/') + secure_filename(f.filename)
        filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
        f.save(filename)
        current_app.logger.info(f'{filename} is saved.')

# 화면에 쓰기위한것 
        # 커피데이터를 정수로 읽기 위해 int로 줌
        coffee_index = pd.read_csv(filename, dtype={'이디야 매장수': int, '스타벅스 매장수':int, '커피빈 매장수': int, '빽다방 매장수':int})
        # 컬러를 따로 주기위해 따로 칼라맵 코드를 만들어서 줌
        color_dict = {'커피지수':'Reds', '이디야 매장수':'Blues', '스타벅스 매장수': 'Greens','커피빈 매장수':'Purples', '빽다방 매장수':'PuBu'}
        # 이미지 파일을 만드는 것
        img_file = os.path.join(current_app.root_path, 'static/img/coffee.png') # 파일이름
        dk.drawKorea(item, coffee_index, color_dict[item], img_file) # 파일이름을 drawKorea에게 전달
        mtime = int(os.stat(img_file).st_mtime)

        #top10 만들기
        # 컬럼명으로 솔팅해서 id랑 item 을 빼옴
        df = coffee_index.sort_values(by=item, ascending=False)[['ID', item]].reset_index()
        top10={}
        for i in range(10): # 랜더링할때 라운딩을 해서 소수점 2자리까지 
            top10[df['ID'][i]] = round(df[item][i], 2)
        return render_template('cartogram/coffee_res.html', menu=menu, weather=get_weather(), 
                                mtime=mtime, item=item, top10=top10)