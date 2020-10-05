from datetime import datetime as dt

from flask import current_app as app, request, make_response, jsonify, render_template
from flask_basicauth import BasicAuth
from . import db
from .database.models.country import Country
from .database.models.country_replica import CountryReplica
from healthcheck import HealthCheck, EnvironmentDump

basic_auth = BasicAuth(app)

health = HealthCheck(app, "/health")
envdump = EnvironmentDump(app, "/env")


@app.route('/status', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@app.route('/country/', methods=['POST'])
@basic_auth.required
def create_user():
    """Create a country."""
    data = request.get_json()
    name = data['name']
    country_id = data['country_id']
    two_letter = data['two_letter']
    try:
        new_country = Country(name=name,
                              country_id=country_id,
                              two_letter=two_letter)
        db.session.add(new_country)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        return {"success": data}

    except BaseException as error:
        #Not best practice!
        print('An exception occurred: {}'.format(error))
        return {"error": "Failed to make Country"}


@app.route('/country/<two_letter>', methods=['GET'])
@basic_auth.required
def show_country(two_letter):
    try:
        country = Country.query.filter_by(two_letter=two_letter).first_or_404()
        return jsonify(country)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        return {"error": "Failed to get Country"}
@app.route('/country_replica/<two_letter>', methods=['GET'])
@basic_auth.required
def show_country_replica(two_letter):
    try:
        country = CountryReplica.query.filter_by(two_letter=two_letter).first_or_404()
        return jsonify(country)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        #Not best practice!
        return {"error": "Failed to get Country Replica"}

