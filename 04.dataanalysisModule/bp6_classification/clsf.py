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

@clsf_bp.route('/titanic', methods=['GET', 'POST'])
def titanic():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/titanic.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/titanic_test.csv')
        scaler = joblib.load('static/model/titanic_scaler.pkl')
        test_data = df.iloc[index, 1:].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, 0]
        lrc = joblib.load('static/model/titanic_lr.pkl')
        svc = joblib.load('static/model/titanic_sv.pkl')
        dtc = joblib.load('static/model/titanic_dt.pkl')
        rfc = joblib.load('static/model/titanic_rf.pkl')
        knc = joblib.load('static/model/titanic_kn.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_dt = dtc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        pred_kn = knc.predict(test_scaled)
        print(label, pred_lr[0], pred_sv[0], pred_dt[0], pred_rf[0],pred_kn[0])
        titanic_dict = {'label':label, 'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_dt':pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}

        tmp = df.iloc[index, 1:].values
        value_list = []
        int_index_list = [0, 1, 3, 4, 6, 7]
        for i in range(8):
            if i in int_index_list:
                value_list.append(int(tmp[i]))
            else:
                value_list.append(tmp[i])
        org = dict(zip(df.columns[1:], value_list))
        return render_template('classification/titanic_res.html', menu=menu, weather=get_weather(), res=titanic_dict, org=org)

@clsf_bp.route('/pima', methods=['GET', 'POST'])
def pima():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/pima.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/pima_test.csv')
        scaler = joblib.load('static/model/pima_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/pima_lr.pkl')
        svc = joblib.load('static/model/pima_sv.pkl')
        dtc = joblib.load('static/model/pima_dt.pkl')
        rfc = joblib.load('static/model/pima_rf.pkl')
        knc = joblib.load('static/model/pima_kn.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_dt = dtc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        pred_kn = knc.predict(test_scaled)
        # print(label, pred_lr[0], pred_sv[0], pred_dt[0], pred_rf[0],pred_kn[0])
        pima_dict = {'label':label, 'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_dt':pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}
        return render_template('classification/pima_res.html', menu=menu, weather=get_weather(), pima_dict=pima_dict)

@clsf_bp.route('/cancer', methods=['GET', 'POST'])
def cancer():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/cancer.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/cancer_test.csv')
        scaler = MinMaxScaler()
        scaled_test = scaler.fit_transform(df.iloc[:, :-1])
        test_data = scaled_test[index, :].reshape(1,-1)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/cancer_lr.pkl')
        svc = joblib.load('static/model/cancer_sv.pkl')
        dtc = joblib.load('static/model/cancer_dt.pkl')
        rfc = joblib.load('static/model/cancer_rf.pkl')
        knc = joblib.load('static/model/cancer_kn.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_dt = dtc.predict(test_data)
        pred_rf = rfc.predict(test_data)
        pred_kn = knc.predict(test_data)
        # print(label, pred_lr[0], pred_sv[0], pred_dt[0])
        option_dict = {'label':label, 'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_dt':pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}
        return render_template('classification/cancer_res.html', menu=menu, weather=get_weather(), option_dict=option_dict)

@clsf_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/iris.html', menu=menu, weather=get_weather())
    else:
        # pass
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/iris_test.csv')
        scaler = joblib.load('static/model/iris_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/iris_lr.pkl')
        svc = joblib.load('static/model/iris_sv.pkl')
        dtc = joblib.load('static/model/iris_dt.pkl')
        rfc = joblib.load('static/model/iris_rf.pkl')
        knc = joblib.load('static/model/iris_kn.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_dt = dtc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        pred_kn = knc.predict(test_scaled)

        species = ['Setosa', 'Versicolor', 'Virginica']
        # print(label, pred_lr[0], pred_sv[0], pred_dt[0], pred_rf[0],pred_kn[0])
        iris_dict = {'label':f'{label} ({species[label]})', 'pred_lr':f'{pred_lr[0]} ({species[pred_lr[0]]})',
                    'pred_sv':f'{pred_sv[0]} ({species[pred_sv[0]]})', 'pred_dt':f'{pred_dt[0]} ({species[pred_dt[0]]})', 
                    'pred_rf':f'{pred_rf[0]} ({species[pred_rf[0]]})', 'pred_kn': f'{pred_kn[0]} ({species[pred_kn[0]]})'}
        return render_template('classification/iris_res.html', menu=menu, weather=get_weather(), iris_dict=iris_dict)

@clsf_bp.route('/wine', methods=['GET', 'POST'])
def wine():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'st':0}
    if request.method == 'GET':
            return render_template('classification/wine.html', menu=menu, weather=get_weather())
    else:
        # pass
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/wine_test.csv')
        scaler = joblib.load('static/model/wine_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/wine_lr.pkl')
        svc = joblib.load('static/model/wine_sv.pkl')
        dtc = joblib.load('static/model/wine_dt.pkl')
        rfc = joblib.load('static/model/wine_rf.pkl')
        knc = joblib.load('static/model/wine_kn.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_dt = dtc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        pred_kn = knc.predict(test_scaled)
        # print(label, pred_lr[0], pred_sv[0], pred_dt[0], pred_rf[0],pred_kn[0])
        wine_dict = {'label':label, 'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_dt':pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}
        return render_template('classification/wine_res.html', menu=menu, weather=get_weather(), wine_dict=wine_dict)
