from flask import render_template, flash, url_for, redirect
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"congratulations {form.username.data}, you've successfully created an account!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Register')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'example@email.com' and form.password.data == 'password':
            flash("You have been logged in", 'success')
            return redirect('home')
        else:
            flash('Something went wrong! Please check email or password!', 'danger')
    return render_template('login.html', form=form, title='Login')
