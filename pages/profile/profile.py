from flask import Blueprint, render_template, session
from utilities.db.db_manager import dbManager

# profile blueprint definition
profile = Blueprint('profile', __name__, static_folder='static', static_url_path='/profile', template_folder='templates')

##-------------------functions-----------------------------
def get_amount_by_func(email, functionq  ):  #
    sqrt = dbManager.fetch('SELECT Finished FROM progress WHERE Email=%s AND FunctionName=%s AND SubFunctionName=%s', (email, functionq, ' שורש'))
    rational = dbManager.fetch('SELECT Finished FROM progress WHERE Email=%s AND FunctionName=%s AND SubFunctionName=%s', (email, functionq, ' מנה'))
    non = dbManager.fetch('SELECT Finished FROM progress WHERE Email=%s AND FunctionName=%s AND SubFunctionName=%s', (email, functionq, ' ללא שורש או מנה'))

    return [len(sqrt), len(rational), len(non)]

# Routes
@profile.route('/profile')
def index():
    email = session.get('user')['Email']
    LastEntry = dbManager.fetch('SELECT LastEntry FROM users WHERE Email=%s', (email,))
    LastEntryStr = str(LastEntry[0][0].day) + '.' + str(LastEntry[0][0].month) + '.' + str(LastEntry[0][0].year)

    totalClues = dbManager.fetch('SELECT COUNT(*) as totalClues FROM clues')
    filteredClues = dbManager.fetch('SELECT COUNT(*)  as filteredClues FROM clues_for_user WHERE Email=%s AND Appear = 0', (email,))

    filteredPercentage= "{:.2f}".format(filteredClues[0][0]*100/totalClues[0][0])
    poly = get_amount_by_func(email, ' פולינום')
    exp = get_amount_by_func(email, ' מעריכית')
    log = get_amount_by_func(email, ' לוגריתמית')
    trigo = get_amount_by_func(email, ' טריגונומטרית')

    return render_template('profile.html', LastEntry=LastEntryStr, filteredPercentage=filteredPercentage, poly=poly, exp=exp, log=log, trigo=trigo  )
