from flask import Blueprint, render_template, redirect, url_for

# mainpage blueprint definition
mainpage = Blueprint('mainpage', __name__, static_folder='static', static_url_path='/mainpage', template_folder='templates')


# Routes

@mainpage.route('/mainpage')
def index():
    return render_template('mainpage.html')


