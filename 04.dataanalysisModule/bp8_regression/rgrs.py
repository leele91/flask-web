from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from my_util.weather import get_weather

rgrs_bp = Blueprint('rgrs_bp', __name__)

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

@rgrs_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':1, 'cu':0, 'st':0}

    if request.method == 'GET':
            return render_template('regression/iris.html', menu=menu, weather=get_weather())
    else:
        # pass
        index = int(request.form['index'])
        feature_name = request.form['feature']
        column_dict = {'sl':'Sepal length', 'sw':'Sepal width', 
                        'pl':'Petal length', 'pw':'Petal width', 
                        'species':['Setosa', 'Versicolor', 'Virginica']}
        column_list = list(column_dict.keys())

        df = pd.read_csv('static/data/iris_train.csv')
        df.columns = column_list
        X = df.drop(columns=feature_name, axis=1).values
        y = df[feature_name].values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/iris_test.csv')
        df_test.columns = column_list
        X_test = df_test.drop(columns=feature_name, axis=1).values[index]
        pred_value = np.dot(X_test, weight.T) + bias

        x_test = list(df_test.iloc[index,:-1].values)
        x_test.append(column_dict['species'][int(df_test.iloc[index,-1])])
        org = dict(zip(column_list, x_test))
        pred = dict(zip(column_list[:-1], [0,0,0,0]))
        pred[feature_name] = np.round(pred_value, 2)
        return render_template('regression/iris_res.html', menu=menu, weather=get_weather(),
                                index=index, org=org, pred=pred, feature=column_dict[feature_name])
kospi_dict, kosdaq_dict, nyse_dict, nasdaq_dict = {}, {}, {}, {}