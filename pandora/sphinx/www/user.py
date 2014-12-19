from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user

from model.user import User


site = Blueprint('user', 'www.user')

@site.route('/<id>')
def profile(id):
    user = User.from_id(id)
    if user is None:
        abort(404)
    return render_template('user/profile.html', user=user)
    
@site.route('/dofollow',methods=['POST'])
@login_required
def dofollow():
    try:
        id = int(request.form['id'])
    except KeyError:
        abort(400)
    followee = User.from_id(id)
    if followee is None:
        abort(404)
    followee.addfollower(current_user.id)
    return 'done!'