from flask import Blueprint, render_template, abort

from model.user import User

site = Blueprint('user', 'www.user')

@site.route('/<id>')
def profile(id):
    user = User.from_id(id)
    if user is None:
        abort(404)
    return render_template('user/profile.html', user=user)