from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime

class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String) 
    blog_comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Blogs = []

    def save_blog(self):
        db.session.add(self)
        db.session.commit(self)
        # Blog.Blogs.append(self)

    @classmethod
    def get_blog(cls,id):
        blogs = Blog.query.filter_by(blog_id=id).all()
        return blogs
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments
class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    blog_id= db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog_title = db.Column(db.String)
    blog_comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    all_comments = []

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        # Comment.all_comments.append(self)

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments

    # def __init__(self,blog_id,title,comment, user_id):
    #     self.blog_id = blog_id
    #     self.title = title
    #     # self.imageurl = imageurl
    #     self.comment = comment

        
    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    blog = db.relationship('Blog',backref = 'user',lazy = "dynamic")

    def __repr__(self):
        return f'User {self.username}'
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure, password)
            
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'