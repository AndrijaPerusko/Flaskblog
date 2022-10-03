from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
