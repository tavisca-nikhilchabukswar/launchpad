from datetime import datetime
from flask import render_template , request , jsonify
from scaling_api import app , ApplicationInfo , Scale
import boto3
import sys


def InitializeEc2Client():
    #session = boto3.Session(profile_name=_AwsProfile)
    client = boto3.client('ec2',region_name = "us-east-1")
    return client

def InitializeASGClient():
    #session = boto3.Session(profile_name=_AwsProfile)
    client = boto3.client('autoscaling',region_name = "us-east-1")
    return client

def InitializeELBClient():
    #session = boto3.Session(profile_name=_AwsProfile)
    client = boto3.client('elb',region_name = "us-east-1")
    return client

def GetApplicationObject(data):
    app = ApplicationInfo.Application()
    app.ApplicationName = data["ApplicationName"]
    app.DesiredCount = data["DesiredCount"]
    app.MinCount = data["MinimumCount"]
    app.MaxCount = data["MaximumCount"]
    app.InstanceType = data["InstanceType"]
    return app

def GetScaleUpObject(data):
    application = GetApplicationObject(data)
    scale = Scale.ScaleEnvironment(application,InitializeEc2Client(),InitializeELBClient(),InitializeASGClient())
    scale.scaling_type = data["ScalingType"]
    return scale

@app.route('/scaleup',methods=['GET','POST'])
def scaleup():
    data =  request.get_json()
    scale_object = GetScaleUpObject(data)
    Status = scale_object.ScaleUpEnvironment()
    Status = True
    if Status:
        return jsonify("application scaled up successfully")
    else:
        return jsonify("Error in Scaling now contact DevOps :) !!! ")

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
