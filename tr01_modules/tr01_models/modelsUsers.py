from .modelsBase import Base, sess
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, \
    Date, Boolean, Table
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from .config import config
import os


def default_username(context):
    return context.get_current_parameters()['email'].split('@')[0]



class Users(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(Text, unique = True, nullable = False)
    password = Column(Text, nullable = False)
    username = Column(Text, default=default_username)
    admin = Column(Boolean, default=False)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    rincons = relationship("UsersToRincons", back_populates="user")
    posts = relationship('RinconsPosts', backref='posts_ref_users', lazy=True)
    post_like = relationship('RinconsPostsLikes', backref='post_like_ref_users', lazy=True)
    post_comment = relationship('RinconsPostsComments', backref='post_comment_ref_users', lazy=True)
    post_comment_like = relationship('RinconsPostsCommentsLikes', backref='post_comment_like_ref_users', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s=Serializer(config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return sess.query(Users).get(user_id)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email}, username: {self.username},' \
        f'rincons: {self.rincons})'


class Rincons(Base):
    __tablename__ = 'rincons'
    id = Column(Integer, primary_key = True)
    name = Column(Text, nullable = False)
    name_no_spaces = Column(Text, nullable = False)
    key = Column(Text)
    manager_id = Column(Integer)#<-- User_id of a user that is manager
    public = Column(Boolean, default=False)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    users = relationship("UsersToRincons", back_populates="rincon")
    # posts = relationship("RinconsToPosts", back_populates="rincon")
    posts = relationship('RinconsPosts', backref='posts_ref_rincons', lazy=True)
    posts_likes = relationship('RinconsPostsLikes', backref='posts_likes_ref_rincons', lazy=True)
    comments = relationship('RinconsPostsComments', backref='comments_ref_rincons', lazy=True)
    comments_likes = relationship('RinconsPostsCommentsLikes', backref='comments_likes_ref_rincons', lazy=True)

    def __repr__(self):
        return f'RinconsTable(id: {self.id}, name: {self.name},' \
        f'manager_id: {self.manager_id})'


class RinconsPosts(Base):
    __tablename__ = 'rincons_posts'
    id = Column(Integer, primary_key = True)
    text = Column(Text)
    image_file_name = Column(Text)# <-- should be lists
    video_file_name = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)# TODO: create ForeignKey to users.id i.e. child to Users parent <--- DONE
    rincon_id = Column(Integer, ForeignKey("rincons.id"), nullable = False)# TODO: create ForeignKey to rincons.id i.e child to Rincons parent <--- DONE
    post_like = relationship("RinconsPostsLikes", backref="post_likes_ref")# DONE
    comments = relationship("RinconsPostsComments", backref="comments_ref")# DONE: 
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow) 
    

    def __repr__(self):
        return f'RinconsPosts(id: {self.id}, rincon_id: {self.rincon_id},' \
        f'user_id: {self.user_id}, text: {self.text})'

class RinconsPostsLikes(Base):
    __tablename__ = 'rincons_posts_likes'
    # id = Column(Integer, primary_key = True)
    # rincon_id = Column(Integer, ForeignKey("rincons.id"), nullable = False)
    rincon_id = Column(Integer, ForeignKey("rincons.id"), primary_key = True)
    post_id = Column(Integer, ForeignKey("rincons_posts.id"), primary_key=True)# TODO: create ForeignKey to RinconsPosts.id i.e. child to RinconsPosts parent
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)# TODO: create ForeignKey to Users.id i.e.child to Users parent
    post_like = Column(Boolean, default=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'RinconsPostsLikes(user_id: {self.user_id}, post_id: {self.post_id},' \
        f' post_like: {self.post_like})'

class RinconsPostsComments(Base):
    __tablename__ = 'rincons_posts_comments'
    id = Column(Integer, primary_key = True)
    post_id = Column(Integer, ForeignKey("rincons_posts.id"), nullable = False)# TODO: create ForeignKey to RinconsPosts.id i.e. child to RinconPosts parent <--- DONE
    rincon_id = Column(Integer, ForeignKey("rincons.id"), nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)# TODO: create ForeignKey to Users.id i.e. child to Users parent <--- DONE
    text = Column(Text)
    image_file_name = Column(Text)# <-- should be lists
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'RinconsPostsComments(id: {self.id}, post_id: {self.post_id},' \
        f'user_id: {self.user_id}, text: {self.text})'

class RinconsPostsCommentsLikes(Base):
    __tablename__ = 'rincons_posts_comments_likes'
    id = Column(Integer, primary_key = True)
    rincon_id = Column(Integer, ForeignKey("rincons.id"), nullable = False)
    post_id = Column(Integer, ForeignKey("rincons_posts.id"), nullable = False)
    comment_id = Column(Integer, ForeignKey("rincons_posts_comments.id"), primary_key = True)# TODO: create ForeignKey to RinconsPostsComments.id i.e. child to RinconsPostsComments parent
    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)# TODO: create ForeignKey to Users.id i.e. child to Users parent
    comment_like = Column(Boolean, default=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'RinconsPostsCommentsLikes(comment_id: {self.comment_id},' \
        f'user_id: {self.user_id}, comment_like: {self.comment_like})'


##########
# Associations
##############

class UsersToRincons(Base):
    __tablename__ = 'users_rincon'
    users_table_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    rincons_table_id = Column(Integer, ForeignKey('rincons.id'), primary_key=True)
    permission = Column(Boolean)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    rincon = relationship("Rincons", back_populates="users")
    user = relationship("Users", back_populates="rincons")

    def __repr__(self):
        return f'UsersToRincons(users_table_id: {self.users_table_id}, rincons_table_id: {self.rincons_table_id})' 


# class RinconsToPosts(Base):
#     __tablename__ = 'rincons_to_posts'
#     rincons_table_id = Column(Integer, ForeignKey('rincons.id'), primary_key=True)
#     rinconsposts_table_id = Column(Integer, ForeignKey('rincons_posts.id'), primary_key=True)

#     post = relationship("RinconsPosts", back_populates="rincons")
#     rincon = relationship("Rincons", back_populates="posts")

#     def __repr__(self):
#         return f'RinconsToPosts(rincons_table_id: {self.rincons_table_id}, rinconsposts_table_id: {self.rinconsposts_table_id})' 

# class PostsToComments(Base):
#     __tablename__ = 'rincons_to_posts'

#     rinconsposts_table_id = Column(Integer, ForeignKey('rincons_posts.id'), primary_key=True)
#     rinconspostscomments_table_id = Column(Integer, ForeignKey('rincons_posts_comments.id'), primary_key=True)

#     comment = relationship("RinconsPostsComments", back_populates="posts")
#     post = relationship("RinconsPosts", back_populates="comments")


#     def __repr__(self):
#         return f'RinconsToPosts(rincons_table_id: {self.rincons_table_id}, rinconsposts_table_id: {self.rinconsposts_table_id})' 

