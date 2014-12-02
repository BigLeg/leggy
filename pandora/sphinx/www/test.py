from flask import render_template
from flask import Blueprint

site = Blueprint('test', 'www.test')

@site.route('/', methods=['GET'])
def index():
    return render_template('test/index.html')

@site.route('/hello/<uid>', methods=['GET'])
def hello(uid):
    return "Hello %s" % uid

@site.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@site.route('/video_play', methods=['GET'])
def video_test():
    return render_template('test/video-play.html', user_id='1', video_name='Week12.webm')

@site.route('/video_upload', methods=['GET'])
def video_upload():
    return render_template('test/video-upload.html')