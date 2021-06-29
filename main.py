from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Predict

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def predict():
    st_name = request.form['stock']
    check1 = Predict.check_stock(st_name)
    return render_template('profile.html', check_1=check1, name=current_user.name, url='../static/images/plot1.png', url2='../static/images/plot2.png')

