from flask import Blueprint
from flask import render_template
from model.video import Video
site = Blueprint('home', 'www.home')

@site.route('/')
def index():
    hottest = Video.hottest()
    newest = Video.newuploaded()
    return render_template('index.html',
                            hottestvideos = hottest,
                            newestvideos = newest)