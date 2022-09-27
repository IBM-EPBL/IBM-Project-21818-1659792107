from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def sigin():
    return render_template('signin.html')

@app.route('/about')
def blog():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)