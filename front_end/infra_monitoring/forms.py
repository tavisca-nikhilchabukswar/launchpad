from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField , RadioField , IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ApplicationForm(FlaskForm):
    application_name = StringField('Application_Name',validators=[DataRequired()])
    application_instance_type = StringField('Application_Instance_Type',validators=[DataRequired()])
    application_instance_count = IntegerField('Application_Instance_Count',validators=[DataRequired()])
    application_desired_container_count = IntegerField('Application_Desired_Container_Count',validators=[DataRequired()])
    application_type = RadioField('Application_Type',choices=[('ec2','EC2'),('ecs','ECS')])
    environment = SelectField('Environment',choices=[('QA','qa'),('Non-Prod','stage'),('Production','prod')])
    submit = SubmitField('Register')