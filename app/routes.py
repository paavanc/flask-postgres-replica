from datetime import datetime as dt

from flask import current_app as app, request, jsonify, render_template, url_for, redirect, g, abort
from flask_basicauth import BasicAuth
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from healthcheck import HealthCheck, EnvironmentDump


basic_auth = BasicAuth(app)
if app.config['DEBUG_MODE'] != app.config['NOT_FOUND']:
    health = HealthCheck(app, "/health")
    envdump = EnvironmentDump(app, "/env")

SELEC_ALL_FROM = "SELECT * FROM todo"
SELECT_FROM_QUERY = "SELECT * FROM todo where id = :x"
SELECT_FROM_QUERY_TASK = "SELECT * FROM todo where task = :x"
CREATE_TEXT = "INSERT INTO todo(task) VALUES (:task)"

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def get_sql_engine(config_key):
    DB_URI = app.config[config_key]
    engine = create_engine(DB_URI)
    return engine

def result_to_dict(resultproxy):
    return ([{**row} for row in resultproxy])

def create_helper(task):
    engine = get_sql_engine('SQLALCHEMY_DATABASE_URI')
    with engine.connect() as conn:
        conn.execute(text(CREATE_TEXT), task=task)


@app.route('/status', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }

@app.route('/', methods = ['GET'])
@basic_auth.required
def index():
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_REPLICA_URI')
        with engine.connect() as conn:
            selection= result_to_dict(conn.execute(text(SELEC_ALL_FROM)).fetchall())
            return render_template('index.html', complete=selection)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to load page")

@app.route('/add_task', methods=['POST'])
@basic_auth.required
def add_task():
    """Create a todo."""
    try:
        task = request.form['todoitem']
        create_helper(task)
        return redirect(url_for('index'))
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to create todo")

@app.route('/todo', methods=['POST'])
@basic_auth.required
def create_todo():
    """Create a todo."""
    try:
        data = request.get_json()
        task = data['task']
        create_helper(task)
        engine = get_sql_engine('SQLALCHEMY_DATABASE_REPLICA_URI')
        #Fetching from replica right away may be a bad idea in prod casue of latency
        with engine.connect() as conn:
            return result_to_dict(conn.execute(text(SELECT_FROM_QUERY_TASK), x=task).fetchall())[0]
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to create todo")


@app.route('/todo/<id>', methods=['GET'])
@basic_auth.required
def show_todo(id):
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_URI')
        with engine.connect() as conn:
            # throw a 400 for now if item doesn't exist
            return result_to_dict(conn.execute(text(SELECT_FROM_QUERY), x=id).fetchall())[0]
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get todo")

@app.route('/todo_replica/<id>', methods=['GET'])
@basic_auth.required
def show_todo_replica(id):
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_REPLICA_URI')
        with engine.connect() as conn:
            # throw a 400 for now if item doesn't exist
            return result_to_dict(conn.execute(text(SELECT_FROM_QUERY), x=id).fetchall())[0]
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get todo Replica")

# Not pagineted
@app.route('/todo_replica', methods=['GET'])
@basic_auth.required
def show_todo_replica_all():
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_REPLICA_URI')
        with engine.connect() as conn:
            return jsonify(result_to_dict(conn.execute(text(SELEC_ALL_FROM)).fetchall()))
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get all todo Replicas")

# Not pagineted
@app.route('/todo', methods=['GET'])
@basic_auth.required
def show_todo_all():
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_URI')
        with engine.connect() as conn:
            return jsonify(result_to_dict(conn.execute(text(SELEC_ALL_FROM)).fetchall()))
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get all todo Replicas")
