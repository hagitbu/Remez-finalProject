from flask import Blueprint, render_template, redirect, url_for

# question blueprint definition
question = Blueprint('question', __name__, static_folder='static', static_url_path='/question', template_folder='templates')


# Routes

@question.route('/question')
def index():
    return render_template('question.html')
