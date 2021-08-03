# import the Flask class from the flask module
from re import template
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

# create the application object
app = Flask(__name__,template_folder='template')

# config
app.secret_key = 'my precious'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# langing page for application for login using cred
@app.route('/')
@login_required
def home():
    return render_template('landing.html')

# route for handling the login page logic
@app.route('/log_in', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'sabya' or request.form['password'] != 'UKCR21':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('log_in.html', error=error)

@app.route('/reportgen', methods=['GET', 'POST'])
@login_required
def reportgen():
    msg = None
    if request.method == 'POST':
        if "opt1" in request.form:
            msg = 'Generating report ...'
        if "opt2" in request.form:
            msg = 'Downloading report ...'
    flash(msg)
    return render_template('reportgen.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('home'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)