import os
import PIL
from PIL import Image
import simplejson
from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug import secure_filename

from util.upload_file import uploadfile


ALLOWED_EXTENSIONS = set(['webm'])

site = Blueprint('video', __name__)

# @site.route('/play', methods=['GET'])
# def play_video(userid,videoid):
#     page_title='NyanNyan'
#     desc='Blablabla'
#     return render_template('_videoplayer.html',video_data = video)
# 
# @site.route('/uservideos', methods=['GET'])
# def list_uservideos(userid,sort='time'):
#     return render_template('_uservideos.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_folder():
    user_id = str(current_user.id)
    if user_id is not None:
        return os.path.join(app.config['VIDEOS_UPLOAD_FOLDER'], user_id)
    else:  # TODO: raise error
        return app.config['VIDEOS_UPLOAD_FOLDER']

def get_path(filename):
    return os.path.join(get_folder(), filename)

def get_non_conflict_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    name = filename
    while os.path.exists(get_path(name)):
        name, extension = os.path.splitext(filename)
        name = '%s_%s%s' % (name, str(i), extension)
        i = i + 1
    return name

@site.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filename = get_non_conflict_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(name=get_path(filename),
                                    type=mimetype,
                                    size=0,
                                    not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = get_path(filename)  # TODO:
                folder = get_folder()
                if not os.path.exists(folder):
                    os.mkdir(folder)
                file.save(uploaded_file_path)

                # create thumbnail after saving
                # if mimetype.startswith('image'):
                #     create_thumbnai(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename,
                                    type=mimetype,
                                    size=size)

            # for validation
            return simplejson.dumps({"files": [result.get_file()]})

    # if request.method == 'GET':
    #     # get all file in ./data directory
    #     files = [ f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
    #
    #     file_display = []
    #
    #     for f in files:
    #         size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
    #         file_saved = uploadfile(name=f, size=size)
    #         file_display.append(file_saved.get_file())
    #
    #     return simplejson.dumps({"files": file_display})

    return render_template('video/upload.html')