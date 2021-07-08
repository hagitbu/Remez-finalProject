from flask import Blueprint, render_template, session, request
from utilities.db.db_manager import dbManager

# contact blueprint definition
contact = Blueprint('contact', __name__, static_folder='static', static_url_path='/contact', template_folder='templates')


# Routes
@contact.route('/contact', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = session.get('user')["Email"]
        ContactDetails = dbManager.fetch('SELECT * FROM contact')
        if ContactDetails:
            contactID = len(ContactDetails) + 1
        else:
            contactID = 1
        UserDit = dbManager.fetch('SELECT * FROM users WHERE Email=%s', (email,))
        Ufirstname = UserDit[0].FirstName
        Ulastname = UserDit[0].LastName
        Uphone = UserDit[0].PhoneNumber
        subject = request.form['subject']
        message = request.form['message']
        dbManager.commit('insert into contacts values (%s, %s, %s, %s, %s, %s)', (contactID, Ufirstname, Ulastname, Uphone, subject, message))
        return render_template('contact.html', User_Detail=UserDit[0])
    elif request.method == 'GET':
        return render_template('contact.html')