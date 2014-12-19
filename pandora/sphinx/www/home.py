from flask import Blueprint
from flask import render_template
from model.video import Video
site = Blueprint('home', 'www.home')

@site.route('/')
def index():
    #Video.hottest()
    #Video.newest()
    return render_template('index.html')