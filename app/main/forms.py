from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField("Blog:", validators = [Required()])
    submit = SubmitField("submit")
    
class UpdateBio(FlaskForm):
    bio = StringField("Bio")
    submit = SubmitField("Update")

class EmailForm(FlaskForm):
    email = StringField("Enter email", validators = [Required()])
    submit = SubmitField("subscribe")

class AddComment(FlaskForm):
    comment = TextAreaField("Comment", validators = [Required()])
    submit = SubmitField("Comment")