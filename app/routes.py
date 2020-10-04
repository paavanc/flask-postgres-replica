from datetime import datetime as dt

from flask import current_app as app, request, make_response, jsonify, render_template

from . import db
from .database.models.account import Country, CountryReplica

@app.route('/status', methods=['GET'])
def hello_world():
    return {
        'hello': 'world'
    }


@app.route('/country/', methods=['POST'])
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
def show_country(two_letter):
    country = Country.query.filter_by(two_letter=two_letter).first_or_404()
    return jsonify(country)

@app.route('/country_replica/<two_letter>', methods=['GET'])
def show_country_replica(two_letter):
    country = CountryReplica.query.filter_by(two_letter=two_letter).first_or_404()
    return jsonify(country)