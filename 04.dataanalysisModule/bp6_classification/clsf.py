from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import os, joblib
import pandas as pd
import pandas_datareader as pdr
from my_util.weather import get_weather

clsf_bp = Blueprint('clsf_bp', __name__)

def get_weather_main():
    ''' weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60) '''
    weather = get_weather()
    return weather

@clsf_bp.route('/cancer', methods=['GET', 'POST'])
def cancer():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/cancer.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/cancer_test.csv')
        scaler = MinMaxScaler()
        scaled_test = scaler.fit_transform(df.iloc[:, :-1])
        test_data = scaled_test[index, :].reshape(1,-1)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/cancer_lr.pkl')
        svc = joblib.load('static/model/cancer_sv.pkl')
        dtc = joblib.load('static/model/cancer_dt.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_dt = dtc.predict(test_data)
        # print(label, pred_lr[0], pred_sv[0], pred_dt[0])
        option_dict = {'label':label, 'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_dt':pred_dt[0]}
        return render_template('classification/cancer_res.html', menu=menu, weather=get_weather(), option_dict=option_dict)
            