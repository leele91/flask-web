from flask import Blueprint, render_template, request, session, g
from flask import current_app
import os, joblib, requests, json
from urllib.parse import quote
import pandas as pd
import numpy as np
from my_util.weather import get_weather

nl_bp = Blueprint('nl_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0, 'st':0, 'nl':1}

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

@nl_bp.route('/translate', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'GET':
        return render_template('nat_lang/nl.html', menu=menu, weather=get_weather())
    else:
        text = request.form['text']
        label = request.form['label']

        # 네이버 파파고
        with open('static/keys/papago_key.json') as nkey:
            json_str = nkey.read(100)
        json_obj = json.loads(json_str)
        client_id = list(json_obj.keys())[0]
        client_secret = json_obj[client_id]
        n_url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        n_target = {'en': 'en', 'ja':'ja', 'zh':'zh-CN', 'fr':'fr', 'es':'es'}
        val = {
            "source": 'ko',
            "target": n_target[label],
            "text": text
        }
        
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }
        response = requests.post(n_url, data=val, headers=headers)
        rescode = response.status_code
        if rescode == 200:
            print(response.text)
        else:
            print("Error : " + response.text)
        
        result = response.json()
        n_text = result['message']['result']['translatedText']

        # 카카오
        with open('static/keys/kakaoaikey.txt') as kfile:
            kai_key = kfile.read(100)
        text = text.replace('\n',''); text = text.replace('\r','')
        k_url = f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang=kr&target_lang={label}'
        result = requests.get(k_url, 
                    headers={"Authorization": "KakaoAK "+ kai_key}).json()

        tr_text_list = result['translated_text'][0]
        k_translated_text = '\n'.join([tmp_text for tmp_text in tr_text_list])

# 카카오 번역2
        ''' with open('static/keys/kakaoaikey.txt') as kfile:
            kai_key = kfile.read(100)
        def generate_url(text, src, dst):
            return f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang={src}&target_lang={dst}'
        
        k_target = {'en': 'en', 'ja':'jp', 'zh':'cn', 'fr':'fr', 'es':'es'}
        result = requests.get(generate_url(text, 'kr', k_target[label]), 
                    headers={"Authorization": "KakaoAK "+ kai_key}).json()

        kaka_text = result['translated_text'][0][0] '''


        n_dt = {'text':text, 'n_text':n_text, 'kaka_text':k_translated_text}
        return render_template('nat_lang/nl_res.html', menu=menu, weather=get_weather(), ndt=n_dt)

@nl_bp.route('/tts', methods=['GET', 'POST'])
def tts():
    if request.method == 'GET':
        return render_template('nat_lang/tts.html', menu=menu, weather=get_weather_main())
    else:
        text = request.form['text']
        speaker = request.form['speaker']
        pitch = request.form['pitch']
        speed = request.form['speed']
        volume = request.form['volume']
        emotion = request.form['emotion']

        with open('static/keys/clova_key.json') as nkey:
            json_str = nkey.read(100)
        json_obj = json.loads(json_str)
        client_id = list(json_obj.keys())[0]
        client_secret = json_obj[client_id]

        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        val = {
            "speaker": speaker, "speed": speed, "text": text,
            "pitch": pitch, "volume": volume, "emotion": emotion
        }
        response = requests.post(url, data=val, headers=headers)
        rescode = response.status_code
        audio_file = os.path.join(current_app.root_path, 'static/img/cpv.mp3')
        if(rescode == 200):
            with open(audio_file, 'wb') as f:
                f.write(response.content)
        mtime = int(os.stat(audio_file).st_mtime)

        return render_template('nat_lang/tts_res.html', menu=menu, weather=get_weather_main(),
                                res=val, mtime=mtime)

