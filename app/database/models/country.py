from app import db

class Country(db.Model):
    """Model for country"""

    __tablename__ = 'country'
    __abstract__ = True


    country_id = db.Column(db.Integer,
                     index=False,
                     unique=False,
                     nullable=False)
    name = db.Column(db.String(64),
                     index=False,
                     unique=False,
                     nullable=False)
    two_letter = db.Column(db.String(64),
                    primary_key=True)

    def __repr__(self):
        return '<Country {}>'.format(self.name)
