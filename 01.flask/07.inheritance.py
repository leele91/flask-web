from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/child1')
def child1():
    return render_template('07.child1.htm')

if __name__ == '__main__':
    app.run(debug=True)