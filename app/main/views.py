from . import main
from flask import render_template,url_for,flash,redirect,request
from .forms import RegistrationForm,LoginForm
from .new_form import PitchForm,CommentForm,UpvoteForm,Downvote
from flask_login import login_user,logout_user,login_required,current_user
from ..models import User,Pitch,Downvote,Upvote,Comment
from .. import db
from ..email import mail_message


@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    pitch = Pitch.query.filter_by().first()
    title = 'pitches all over in 60 seconds'
    pickuplines = Pitch.query.filter_by(category="pickuplines")
    interviewpitch = Pitch.query.filter_by(category = "interviewpitch")
    promotionpitch = Pitch.query.filter_by(category = "promotionpitch")
    webapp_pitch = Pitch.query.filter_by(category = "productpitch")

    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
    

    return render_template('index.html', title = title, pitch = pitch, pickuplines=pickuplines, interviewpitch= interviewpitch, promotionpitch = promotionpitch, productpitch = webapp_pitch, upvotes=upvotes)
    

    

# **************************************************************************************************************************************************
# Registration and login/logout routes
# **************************************************************************************************************************************************

#....
@main.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Pitch Login"
    return render_template('login.html',login_form = login_form,title=title)




@main.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Pitches","email/welcome_user",user.email,user=user)

        flash(f'Account created for {form.username.data}! You are now able to log in ')
        return redirect(url_for('main.login'))
        title = "New Account"
    return render_template('register.html',form = form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

# ************************************************************************************************************************

@main.route('/pitches/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    my_upvotes = Upvote.query.filter_by(pitch_id = Pitch.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        new_pitch = Pitch(owner_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_pitch)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('pitches.html',form=form)


@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comments.html', form = form, comment = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))



@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))

# ***********************************************************************************************************************************************

# ********************************************************************************************************************************************************

