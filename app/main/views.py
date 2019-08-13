from flask import render_template,request,redirect,url_for,abort
from app import create_app
from . import main
from ..models import Comment, User,Blog
from .forms import UpdateBio,BlogForm,AddComment,EmailForm
from flask_login import login_required, current_user
from .. import db,photos
from ..request import get_quote
from datetime import datetime
#single user
import markdown2

# homepage function
@main.route('/')
def index():
    title ='Home - Welcome to motoblog'
    name  = "Quote"
    quote = get_quote()
    blog= Blog.query.all()
    print(dir(blog))
    return render_template('index.html', blog=blog, quote=quote)



# user profile page function
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

#update profile
@login_required
@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

# user login
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

# blog post comment functions
@main.route('/comment/<int:id>')
def single_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.blog_comment, extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html', comment=comment, format_comment=format_comment)

#add blog
@main.route("/add/blog/",methods = ["GET","POST"])
@login_required
def add_blog():
    # print(current_user.id)
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        if "photo" in request.files:
            pic = photos.save(request.files["photo"])
            file_path = f"photos/{pic}"
            image = file_path
        new_blog = Blog(blog_title = form.title.data, user_id = current_user.id)
        db.session.add(new_blog)
        db.session.commit()
        # new_blog.save_blog(id)
        # emails = Email.query.all()
        return redirect(url_for('main.index'))
    return render_template("add_blog.html",form = form)

@main.route("/delete/<id>")
def delete_blog(id):
    blog = Blog.query.filter_by(id = id).first()
    user_id = blog.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.profile', id = user_id))
#display blog -> blog.html
@main.route("/blog/<int:id>",methods = ["GET","POST"])
def display(id):
    user = User.query.filter_by(id=id).first()
    blog = Blog.query.filter_by(id=id).first()
    comment = Comment.get_comments(id=id)

    form = AddComment()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_title = blog.blog_title
        new_comment = Comment(blog_id=blog.id, blog_title=blog_title,blog_comment = comment, user_id=current_user.id)
        print(new_comment.blog_comment)
        new_comment.save_comment()
        return redirect(url_for('main.index'))
    blog_title = blog.blog_title
    return render_template("blog.html", blog_title = blog_title, blog = blog,form = form, comments=comment)

# delete comment
@main.route("/delete/comment/<id>")
def delete_comment(id):
    blog_id = comment.blog.id
    db.session.delete(comment)
    db.session.commit()
    comment = Comment.query.filter_by(id = id).first()
    return redirect(url_for("main.display", id = blog_id))
