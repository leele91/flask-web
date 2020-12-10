from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def index():
    img_file = os.path.join(app.root_path, 'static/img/cat.jpg')
    mtime =int(os.stat(img_file).st_mtime)
    return render_template('05.index.htm', mtime = mtime) # mtime를 넣어주면 이미지경로가 바뀔때마다 리플레쉬됨 /html에도 동일적용

if __name__ == '__main__':
    app.run(debug=True)