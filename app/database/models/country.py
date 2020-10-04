from app import db

class Country(db.Model):
    """Model for country"""

    __tablename__ = 'country'

    country_id = db.Column(db.Integer,
                     index=True,
                     unique=True,
                     nullable=False)
    name = db.Column(db.String(64),
                     index=True,
                     unique=True,
                     nullable=False)
    two_letter = db.Column(db.String(64),
                    primary_key=True)

    def __repr__(self):
        return '<Country {}>'.format(self.name)