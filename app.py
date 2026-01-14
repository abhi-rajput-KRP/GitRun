from flask import Flask , redirect , render_template , url_for, request,session,jsonify
import requests , dotenv
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials,firestore,auth

app = Flask(__name__)

app.secret_key = "my_secret_key"

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
cred = credentials.Certificate(dotenv.get_key(".env", "FIREBASE_SDK"))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def login():
    if session.get('uid') is not None:
        return redirect(url_for('leaderboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    if session.get('uid') is not None:
        return redirect(url_for('leaderboard'))
    if request.method == 'POST':
        data = request.form
        user = data.get('user').strip()
        mail = data.get('mail').strip()
        password = data.get('password').strip()
        auth_user = auth.create_user({
            'email':mail,
            'password':password
        })
        session['uid'] = auth_user.uid
        db.collection('Users').document(session.get('uid')).set({
            'user_name':user,
            'email':mail
        })
        return redirect(url_for('/leaderboard'))
    return render_template('register.html')

@app.route('/leaderboard')
def leaderboard():
    if session.get('uid') is None:
        return redirect(url_for('login'))
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)