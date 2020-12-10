from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('02.index.htm')

@ap.route('/welcome')
def welcome():
    return render_template('02.welcome.htm')

if __name__ == '__main__':
    app.run(debug=True)