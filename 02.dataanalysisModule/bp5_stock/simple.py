from flask import Blueprint, render_template

#simple_bp = Blueprint('simple_bp', __name__, template_folder='templates') #개별 폴더
simple_bp = Blueprint('simple_bp', __name__) # 원래의 templates 위치에서

@simple_bp.route('/')
def simple():
    return render_template('stock/simple.html')