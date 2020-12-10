from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    dt = {'key1': 'value1', 'key2': 'value2'} # node에서 사용했던 오브젝트랑 같음 / dt['key1'], dt['key2']
    return render_template('06.hello.htm', name=name, dt=dt)

if __name__ == '__main__':
    app.run(debug=True)