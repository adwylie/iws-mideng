from flask_wtf import FlaskForm, RecaptchaField
from wtforms import DateTimeField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import HiddenInput
from wtforms.widgets.html5 import NumberInput

from .models import Client, User, ProductArea


def user_choices():
    return User.query.all()


def client_choices():
    return Client.query.all()


def product_areas_choices():
    return ProductArea.query.all()


class FeatureRequestForm(FlaskForm):
    id = IntegerField(validators=[Optional()], widget=HiddenInput())
    title = StringField('Title', validators=[DataRequired(), Length(max=60)])
    user = QuerySelectField(
        'User',
        validators=[DataRequired()],
        query_factory=user_choices,
        get_label='full_name'
    )
    client = QuerySelectField(
        'Client',
        validators=[DataRequired()],
        query_factory=client_choices,
        get_label='name'
    )
    priority = IntegerField(
        'Priority',
        default=1,
        validators=[Optional()],
        widget=NumberInput(step=1, min=1)
    )
    target_date = DateTimeField(
        'Target Date',
        validators=[DataRequired()],
        description='Please enter the target date using a 24-hour time.',
        render_kw={'placeholder': '2030-08-20 19:56:20'}
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        render_kw={'rows': 10}
    )

    product_areas = QuerySelectMultipleField(
        'Product Areas',
        query_factory=product_areas_choices,
        get_label='name',
        description='Hold down control (command on mac) to select or '
                    'deselect multiple options.'
    )

    # TODO: Make description required (update tests, model, form). IMPORTANT
    recaptcha = RecaptchaField()
