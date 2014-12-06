import os
from flask import current_app as app

ALLOWED_EXTENSIONS = set(['webm'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_upload_folder(user):
    user_id = str(user.id)
    if user_id is not None:
        return os.path.join(app.config['VIDEOS_UPLOAD_FOLDER'], user_id)
    else:  # TODO: raise error
        return app.config['VIDEOS_UPLOAD_FOLDER']

def get_upload_path(filename, user):
    return os.path.join(get_upload_folder(user), filename)

def get_non_conflict_name(filename, user):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    name = filename
    while os.path.exists(get_upload_path(name, user)):
        name, extension = os.path.splitext(filename)
        name = '%s_%s%s' % (name, str(i), extension)
        i = i + 1
    return name

def get_serve_folder(user):
    user_id = str(user.id)
    if user_id is not None:
        return os.path.join(app.config['VIDEOS_SERVE_FOLDER'], user_id)
    else: # TODO: raise error
        return app.config['VIDEOS_SERVE_FOLDER']

def get_serve_path(filename, user):
    return os.path.join(get_serve_folder(user), filename)

class UploadResponse():
    def __init__(self, name, type=None, size=None, not_allowed_msg=None, url=None, delete_url=None):
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = url
        # TODO
        self.thumbnail_url = "thumbnail/%s" % name
        self.delete_url = delete_url
        self.delete_type = "DELETE"

    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False

    def get_file(self):
        if self.type != None:
            # POST an image
            if self.type.startswith('image'):
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "thumbnailUrl": self.thumbnail_url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type,}

            # POST an normal file
            elif self.not_allowed_msg == None:
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size,}

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type,}

        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type,}
