from flask import Flask


###### App setup
application = app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
## Homepage
from pages.homepage.homepage import homepage
app.register_blueprint(homepage)

## About
from pages.about.about import about
app.register_blueprint(about)

## Contact
from pages.contact.contact import contact
app.register_blueprint(contact)

## Mainpage
from pages.mainpage.mainpage import mainpage
app.register_blueprint(mainpage)

## Profile
from pages.profile.profile import profile
app.register_blueprint(profile)

## Question
from pages.clue.clue import clue
app.register_blueprint(clue)

## Sign_up
from pages.sign_up.sign_up import sign_up
app.register_blueprint(sign_up)

## Log_out
from pages.log_out.log_out import log_out
app.register_blueprint(log_out)

## Log_in
from pages.log_in.log_in import log_in
app.register_blueprint(log_in)

## Page error handlers
from pages.page_error_handlers.page_error_handlers import page_error_handlers
app.register_blueprint(page_error_handlers)

###### Components
## Main menu
from components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)
