#need: layout.html, login.html, register.html

from flask import Flask, render_template, url_for, redirect, request, session
import utils

app = Flask(__name__)
app.secret_key = 'MONGOLIA'

@app.route('/')
def home():
    return redirect(url_for('login'))

def get_form_value(key):
    return request.form[key].encode('ascii','ignore')

def logged_in():
    if 'username' in session and not utils.checkUser(session['username']):
        session.pop('username', None)
    return 'username' in session and session['username'] != None

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = get_form_value('username')
        password = get_form_value('password')
        if utils.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('blog'))
        else:
            error = 'Incorrect username or password.'
    return render_template('login.html', title='Login', error=error)
                
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = get_form_value('username')
        password = get_form_value('password')
        password_confirm = get_form_value('password-confirm')
        if checkUser(username):
            error = 'An account already exists with that username.'
        elif password != password_confirm:
            error = 'The two passwords are not equal.'
        else:            
            register(username, password)
            session['username'] = username
            return redirect(url_for('home'))
    if logged_in():
        return redirect(url_for('blog'))
    return render_template('register.html', title='Register', error=error)

@app.route('/blog')
def blog():
        return render_template('index.html')

@app.route('/accounts')
def accounts():
    users = get_users_as_list()
    a = ""
    for user in users:
        a += user + "<br>"
    return a
        
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
