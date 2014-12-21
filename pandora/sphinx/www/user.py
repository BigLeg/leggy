from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user

from model.user import User
from model.notification import Notification
import json


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
    current_user.follow(followee)
    followee.addnewnote(user_from=current_user.id,
                        type=Notification.TYPE_FOLLOW,
                        )
    return 'done!'
    
@site.route('/msglist',methods =['GET'])
@login_required
def msglist():
    msglist = current_user.get_allmsg()
    page = render_template('user/messages.html',msglist=msglist)
    
    for msg in msglist:
        msg.read = True
        
    return page
    
@site.route('/getnewmsg',methods =['POST'])
@login_required
def getnewmsg():
    msglist = current_user.get_unreadmsg()
    li = []
    for note in msglist:
        element = dict()
        element['from'] = note.userid_from
        element['type'] = note.type
        element['time'] = str(note.time)
        element['read'] = note.read
        li.append(element)
    return json.dumps(li)
    
@site.route('/userlist/<id>/<type>',methods=['GET'])
def userlist(id,type):
    user = User.from_id(id)
    if(type == 'followers'):
        list = user.followers
    elif(type == 'followees'):
        list = user.followees
    else:
        #type == 'friends'
        list = user.getfriends()
    return render_template('user/userlist.html',user=user,type=type,userlist=list)
    
@site.route('/videolist/<userid>',methods=['GET'])
def videolist(userid):
    user = User.from_id(userid)
    return render_template('video/videolist.html',videolist = user.videos)