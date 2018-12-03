from flask import render_template, url_for, flash, redirect
from infra_monitoring import app
from infra_monitoring.forms import RegistrationForm, LoginForm ,ApplicationForm
from infra_monitoring import aws_infrastrcture
from infra_monitoring import application
import requests


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

def get_form_data(form):
    app_object = application.tavisca_app()
    app_object.app_name = form.application_name.data
    app_object.app_type = form.application_type.data
    app_object.app_instance_type = form.application_instance_type.data
    app_object.app_instance_count = form.application_instance_count.data
    app_object.app_env = form.environment.data
    app_object.app_desired_containers = form.application_desired_container_count.data
    return app_object


@app.route("/")
@app.route("/home")
def home():
    #my_applications = application.tavisca_app()
    #instances = aws_infrastrcture.aws(my_applications)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/applications" , methods=['GET','POST'])
def applications():
    form = ApplicationForm()
    form_data = get_form_data(form)
    if form.validate_on_submit():
        flash(f'Application registered for {form.application_name.data}!', 'success')
        response = requests.post("127.0.0.1:6000/register",data=form_data)
        return redirect(url_for('home'))
    return render_template('applications.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)