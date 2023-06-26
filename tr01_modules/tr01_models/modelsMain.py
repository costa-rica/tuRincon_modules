from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import relationship, backref, sessionmaker
from .modelsBase import Base, sess, engine

from .modelsUsers import Users, Rincons, RinconsPosts, RinconsPostsLikes, \
    RinconsPostsComments, RinconsPostsCommentsLikes, UsersToRincons
import os
from flask_login import LoginManager


login_manager= LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(any_name_for_id_obj):# any_name_for_id_obj can be any name because its an arg that is the user id.
    # This is probably created somewhere inside flask_login when the user gets logged in. But i've not been able to track it.
    return sess.query(Users).filter_by(id = any_name_for_id_obj).first()

