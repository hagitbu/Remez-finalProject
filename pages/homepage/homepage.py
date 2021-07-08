from flask import Blueprint, render_template,request, redirect, url_for, session
from utilities.db.db_manager import dbManager
from datetime import datetime

# homepage blueprint definition
homepage = Blueprint('homepage', __name__, static_folder='static', static_url_path='/homepage', template_folder='templates')


# Routes
@homepage.route('/home')
@homepage.route('/homepage')
@homepage.route('/')
def index():
    if session.get('user'): ## if user is logged in
        return redirect(url_for('mainpage.index'))
    elif 'userNotFound' in request.args: ##if the user's email or password is incorrect
        tab_name = request.args['userNotFound']
        return render_template('homepage.html', tab_name=tab_name)
    else:
        return render_template('homepage.html')


@homepage.route('/log_in_form', methods=['POST'])
def log_in_form():
    if request.method == 'POST':
        email = request.form['Email']
        psw = request.form['Password']
        user = dbManager.fetch('SELECT * FROM users WHERE Email=%s AND Password=%s', (email,psw))
        if user and len(user):
            dbManager.commit('UPDATE users SET LastEntry =%s  WHERE Email=%s', (datetime.today().strftime('%y-%m-%d'), email))
            session['logged_in'] = True
            session['user'] = {
                'FirstName': user[0].FirstName,
                'LastName': user[0].LastName,
                'Email': user[0].Email,
                'City': user[0].City,
                'School': user[0].School,
                'PhoneNumber': user[0].PhoneNumber,
                'Password': user[0].Password,
            }

            return redirect(url_for('mainpage.index'))
        else:
            return redirect('/homepage?userNotFound=true')
    return render_template('homepage.html')

