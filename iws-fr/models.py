from flask_sqlalchemy import SQLAlchemy
from .views import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite.db'
db = SQLAlchemy(app)


class Client:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __str__(self):
        return '<Client {}>'.format(self.name)


class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client = db.relationship('Client', backref=db.backref('feature_requests'), lazy=True)

    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)  # update priorities on save
    target_date = db.Column(db.Date, nullable=False)  # must be >= today
    product_areas = db.relationship(
        'ProductArea',
        secondary=fr_pa_map,
        lazy='subquery',
        backref=db.backref('feature_requests', lazy=True)
    )

    # TODO: Test constraints.
    __table_args__ = (
        db.CheckConstraint(priority > 0, name='positive_priority'),
        db.UniqueConstraint('client_id', 'priority', 'unique_client_priorities')
    )

    def __str__(self):
        return '<FeatureRequest {}>'.format(self.title)


# Many-to-many relation (through table) between FeatureRequest and ProductArea.
fr_pa_map = db.Table('fr_pa_map',
    db.Column('feature_request_id', db.Integer, db.ForeignKey('FeatureRequest.id')),
    db.Column('product_area_id', db.Integer, db.ForeignKey('ProductArea.id'))
)


class ProductArea:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __str__(self):
        return '<ProductArea {}>'.format(self.name)
