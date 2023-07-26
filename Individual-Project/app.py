from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey" : "AIzaSyBu7zkO9vCWycyImYQPGAG_ACERK93UsA0",
  "authDomain" : "miniproject-89667.firebaseapp.com",
  "projectId" : "miniproject-89667",
  "storageBucket" : "miniproject-89667.appspot.com",
  "messagingSenderId" : "902940848822",
  "appId" : "1:902940848822:web:077cc7b854cb70e506ac17",
  "measurementId" : "G-FCBP89TD86",
  "databaseURL" : "https://miniproject-89667-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))

        except:
            error = "Authentication failed"

    return render_template("log-in.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        bio = request.form['bio']
        password = request.form['password']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"username" : username, "email" : email, "bio" : bio}
            db.child("Users").child(UID).set(user)  
            return redirect(url_for('home'))

        except:
            error = "Authentication failed"

    return render_template("sign-up.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signup'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        title = request.form['title']
        image = request.form['image']
        username = request.form['username']

        try:
            UID = login_session['user']['localId']
            post = {"title" : title, "image" : image, "username" : username}
            db.child("Post").push(post)
            return redirect(url_for('profile'))

        except:
            error = "Authentication failed"

    UID = login_session['user']['localId']
    info = db.child("Users").child(UID).get().val()
    return render_template("profile.html", info=info)

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        post = db.child("Post").get().val()
        return render_template("home.html", posts=post)

    except:
        error = "Authentication failed"

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)