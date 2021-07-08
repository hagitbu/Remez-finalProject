from flask import Blueprint, render_template,request, redirect, url_for, session
from utilities.db.db_manager import dbManager
from datetime import datetime

# log_in blueprint definition
log_in = Blueprint('log_in', __name__, static_folder='static', static_url_path='/log_in', template_folder='templates')

# Routes

@log_in.route('/log_in')
def index():
    if 'userNotFound' in request.args:
        tab_name = request.args['userNotFound']
        return render_template('log_in.html', tab_name=tab_name)
    return render_template('log_in.html')


@log_in.route('/log_in_form_2', methods=['POST'])
def log_in_form():
    if request.method == 'POST':
        email = request.form['Email']
        psw = request.form['Password']
        user = dbManager.fetch('SELECT * FROM users WHERE Email=%s AND Password=%s', (email,psw))
        if user and len(user):
            dbManager.commit('UPDATE users SET LastEntry =%s  WHERE Email=%s', (datetime.today().strftime('%d-%m-%Y'), email))
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
            return redirect('/log_in?userNotFound=true')
    return render_template('log_in.html')

