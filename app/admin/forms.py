from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    BooleanField,

)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    DataRequired)

from app import db
from app.models import Role, User , Permission

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    roles = SelectMultipleField('Select Role',
                                     coerce=int,
                                     option_widget=widgets.CheckboxInput(),
                                     widget=widgets.ListWidget(prefix_label=False))

    submit = SubmitField('Update role')

class ChangeAccountGroupForm(FlaskForm):
    groups = SelectMultipleField('Select Group',
                                     coerce=int,
                                     option_widget=widgets.CheckboxInput(),
                                     widget=widgets.ListWidget(prefix_label=False))

    submit = SubmitField('Update group')

class ChangeAccountStatusForm(FlaskForm):
    active = BooleanField('Account status?')

    submit = SubmitField('Update status')


class InviteUserForm(FlaskForm):
    #test = db.session.query(Role).order_by('permissions')
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')

class NewRoleForm(FlaskForm):
    role_name = StringField(
        'Role', validators=[InputRequired(),
                                  Length(1, 64)])
    permission = SelectField('Permission type',validators=[InputRequired()],coerce=int, choices=[(Permission.GENERAL,'GENERAL'),(Permission.ADMINISTER,'ADMINISTRATOR')])
    default = BooleanField('Default Role?')


    submit = SubmitField('Add Role')

class NewGroupForm(FlaskForm):
    group_name = StringField('Group', validators=[InputRequired(),Length(1, 64)])

    submit = SubmitField('Add Group')
