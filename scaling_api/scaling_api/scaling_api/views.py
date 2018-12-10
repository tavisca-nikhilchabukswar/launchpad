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

def GetScaleObject(data):
    application = GetApplicationObject(data)
    scale = Scale.ScaleEnvironment(application,InitializeEc2Client(),InitializeELBClient(),InitializeASGClient())
    scale.scaling_type = data["ScalingType"]
    return scale

@app.route('/scaleup',methods=['GET','POST'])
def scaleup():
    data =  request.get_json()
    scale_object = GetScaleObject(data)
    Status = scale_object.ScaleUpEnvironment()
    Status = True
    if Status:
        return jsonify("application scaled up successfully")
    else:
        return jsonify("Error in Scaling now contact DevOps :) !!! ")

@app.route('/scaledown',methods=['GET','POST'])
def scaledown():
    data =  request.get_json()
    scale_object = GetScaleObject(data)
    Status = scale_object.ScaleDownEnvironment()
    Status = True
    if Status:
        return jsonify("application scaled up successfully")
    else:
        return jsonify("Error in Scaling now contact DevOps :) !!! ")
