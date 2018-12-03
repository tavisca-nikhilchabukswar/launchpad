import requests

if __name__ == "__main__":
    form_data = {"name":"be","type":"ec2"}
    response = requests.post("127.0.0.1:6000/register",data=form_data)
    print ("hi")