from flask import current_app, Blueprint, render_template

main = Blueprint('main', import_name=__name__)


@main.route('/')
def index():
    return render_template('index.html')

