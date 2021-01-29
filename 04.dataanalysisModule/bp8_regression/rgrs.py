from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

@rgrs_bp.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':1, 'cu':0, 'st':0}

    if request.method == 'GET':
            return render_template('regression/diabetes.html', menu=menu, weather=get_weather())
    else:
        # pass
        index = int(request.form['index'] or '0')
        feature_name = request.form['feature']
        df = pd.read_csv('static/data/diabetes_train.csv')
        X = df[feature_name].values.reshape(-1, 1)
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/diabetes_test.csv')
        X_test = df_test[feature_name][index]
        y_test = df_test.target[index]
        # pred = X_test * weight[0] + bias
        pred = np.round(X_test * weight[0] + bias, 2)

        # 시각화 
        y_min = np.min(X) * weight[0] + bias
        y_max = np.max(X) * weight[0] + bias

        plt.figure()
        plt.scatter(X, y, label='train')
        plt.plot([np.min(X), np.max(X)], [y_min, y_max], 'r', lw=3)
        plt.scatter([X_test], [y_test], c='r', marker='*', s=100, label='test')
        plt.grid()
        plt.legend()
        plt.title(f'{feature_name}')
        img_file = os.path.join(current_app.root_path, 'static/img/diabetes.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index, 'feature':feature_name, 'y':y_test, 'pred':pred}
        return render_template('regression/diabetes_res.html', menu=menu, weather=get_weather(),
                                mtime=mtime, res=result_dict)

@rgrs_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':1, 'cu':0, 'st':0}

    if request.method == 'GET':
            return render_template('regression/iris.html', menu=menu, weather=get_weather())
    else:
        # pass
        index = int(request.form['index'] or '0')
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



@rgrs_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':1, 'cu':0, 'st':0}

    if request.method == 'GET':
        feature_list = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE',
                        'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
        return render_template('regression/boston.html', menu=menu, weather=get_weather(), feature_list=feature_list)
    else:
        # pass
        index = int(request.form['index'] or '0')
        feature_list = request.form.getlist('feature')
        df = pd.read_csv('static/data/boston_train.csv')
        X = df[feature_list].values
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/boston_test.csv')
        X_test = df_test[feature_list].values[index, :]
        y_test = df_test.target[index]
        pred = np.dot(X_test, weight.T) + bias
        pred = np.round(pred, 2)

        result_dict = {'index':index, 'feature':feature_list, 'y':y_test, 'pred':pred}
        org = dict(zip(df.columns[:-1], df_test.iloc[index, :-1]))
        return render_template('regression/boston_res.html', menu=menu, weather=get_weather(),
                                res=result_dict, org=org)

kospi_dict, kosdaq_dict, nyse_dict, nasdaq_dict = {}, {}, {}, {}