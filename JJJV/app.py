from flask import Flask, render_template, url_for, redirect, request, session
import utils
app = Flask(__name__)
app.secret_key = 'MONGOLIA'


def get_form_value(key):
    return request.form[key].encode('ascii','ignore')

<<<<<<< HEAD
def logged_in():
	if 'username' in session and not username_exists(session['username']):
		session.pop('username', None)
	return 'username' in session and session['username'] != None

@app.route('/')
def home():
    return redirect(url_for('login'))
=======
>>>>>>> 68ef7325997e88fb0ddf089ba497bea551febd8b
@app.route('/login', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'POST':
                username = get_form_value('username')
                password = get_form_value('password')
                if validate_user(username, password):
                        session['username'] = username
                else:
                        error = 'Incorrect username or password.'
        if logged_in():
                return redirect(url_for('blog'))
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
                if username_exists(username):
                        error = 'An account already exists with that username.'
                elif password != password_confirm:
                        error = 'The two passwords are not equal.'
                else:
                        create_user(username, password)
                        session['username'] = username
        if logged_in():
                return redirect(url_for('blog'))
        return render_template('register.html', title='Register', error=error)

@app.route('/blog')
def blog():
        if not logged_in():
                return redirect(url_for('login'))

@app.route('/accounts')
def accounts():
        users = get_users_as_list()
        a = ""
        for user in users:
                a += user + "<br>"
        return a

if __name__ == '__main__':
        init_auth(app)
        
        app.jinja_env.line_statement_prefix = '='
        app.debug = True
        app.run(host='0.0.0.0')


