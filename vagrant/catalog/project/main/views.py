from flask import current_app, Blueprint, render_template
from flask import session as login_session
from flask import make_response
from models import User
import json

main = Blueprint('main', import_name=__name__)


@main.route("/clear_session")
def clear_session():
    login_session.clear()
    response = make_response(json.dumps('Session cleared.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@main.route('/')
def index():
    # noinspection PyProtectedMember
    app = current_app._get_current_object()
    session = app.db_session()
    count = session.query(User.id).count()

    return render_template('index.html')

