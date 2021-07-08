from flask import Blueprint, render_template,request, redirect, url_for,session
from utilities.db.db_manager import dbManager
from datetime import datetime
# sign_up blueprint definition

sign_up = Blueprint('sign_up', __name__, static_folder='static', static_url_path='/sign_up', template_folder='templates')


# Routes
@sign_up.route('/sign_up')
def index():
    if 'emailexist' in request.args:
        tab_name = request.args['emailexist']
        return render_template('sign_up.html', tab_name=tab_name)
    return render_template('sign_up.html')


@sign_up.route('/sign_up_form', methods=['POST'])
def sign_up_form():
    if request.method == 'POST':
        email = request.form['Email']
        psw = request.form['Password']
        fName = request.form['FirstName']
        lName = request.form['LastName']
        city = request.form['City']
        school = request.form['School']
        phone = request.form['PhoneNumber']
        # now = datetime.now()


        checkUser = dbManager.fetch('SELECT * FROM users WHERE Email=%s ', (email,))
        print(checkUser)

        if checkUser == []:

            dbManager.commit('INSERT INTO users VALUES (%s, %s,%s, %s, %s, %s, %s, %s)', (email, psw, fName, lName, city, school, phone, datetime.today().strftime('%Y-%m-%d')))

            # cluesList = dbManager.fetch('SELECT TopicID, ClueID FROM clues')
            # print(cluesList)
            # for i in cluesList:
            #     dbManager.commit('INSERT INTO clues_for_user VALUES (%s, %s, %s, %s, %s)', (email, i[0], i[1], True, 0))

            return redirect(url_for('log_in.index'))
        else:
            return redirect('/sign_up?emailexist=true')


