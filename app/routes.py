from datetime import datetime as dt

from flask import current_app as app, request, jsonify
from flask_basicauth import BasicAuth
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from healthcheck import HealthCheck, EnvironmentDump

basic_auth = BasicAuth(app)
if app.config['DEBUG_MODE'] != app.config['NOT_FOUND']:
    health = HealthCheck(app, "/health")
    envdump = EnvironmentDump(app, "/env")

SELECT_FROM_QUERY = "SELECT * FROM country where two_letter = :x"
CREATE_TEXT = "INSERT INTO COUNTRY(name, two_letter, country_id) VALUES (:name, :two_letter, :country_id)"

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
    d, a = {}, []
    for rowproxy in resultproxy:
    # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
        # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return d


@app.route('/status', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@app.route('/country', methods=['POST'])
@basic_auth.required
def create_user():
    """Create a country."""
    try:
        data = request.get_json()
        name = data['name']
        country_id = data['country_id']
        two_letter = data['two_letter']
        engine = get_sql_engine('SQLALCHEMY_DATABASE_URI')
        with engine.connect() as conn:
            conn.execute(text(CREATE_TEXT), name=name, two_letter=two_letter, country_id=country_id)
            return {"success": data}
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to create Country")


@app.route('/country/<two_letter>', methods=['GET'])
@basic_auth.required
def show_country(two_letter):
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_URI')
        with engine.connect() as conn:
            return result_to_dict(conn.execute(text(SELECT_FROM_QUERY), x=two_letter).fetchall())
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get Country")
@app.route('/country_replica/<two_letter>', methods=['GET'])
@basic_auth.required
def show_country_replica(two_letter):
    try:
        engine = get_sql_engine('SQLALCHEMY_DATABASE_REPLICA_URI')
        with engine.connect() as conn:
            return result_to_dict(conn.execute(text(SELECT_FROM_QUERY), x=two_letter).fetchall())
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        raise InvalidUsage("Failed to get Country Replica")
