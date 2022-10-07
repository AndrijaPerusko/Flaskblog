from flask import redirect, url_for, render_template, flash, request
from flask_login import current_user, logout_user, login_required, login_user
from flaskblog.users import bp
from flaskblog.models import User, Post
from flaskblog import bcrypt, db
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.users.utils import save_picture

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you've successfully created an account!", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Something went wrong! Please check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_f = save_picture(form.picture.data)
            current_user.image_file = picture_f
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@bp.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)
