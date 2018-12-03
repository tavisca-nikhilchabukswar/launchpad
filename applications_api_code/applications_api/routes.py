from applications_api import app
from applications_api import application
from flask import request

@app.route('/register',methods=['GET', 'POST'])
def register():
    request_data = request.data
    print (type(request_data))
    print (request_data)
    obj = application.tavisca_app("nik")
    return "<h1> hi </h2>"
