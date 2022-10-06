from flask import render_template, flash, url_for, redirect, request
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog import app, bcrypt, db
from flaskblog.models import User, Post
from flask_login import current_user, login_user, logout_user

posts = [
    {
        'author': 'John Doe',
        'title': 'Post#1',
        'body': 'First post!',
        'date': '1.1.2019.'
    },
    {
        'author': 'Mike Dowson',
        'title': 'Post#2',
        'body': 'Second post!',
        'date': '11.1.2019.'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you've successfully created an account!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Something went wrong! Please check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
