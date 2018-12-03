import boto3
class aws:
    def __init__(self,application):
        self.ec2_client = boto3.client('ec2')
        self.application = application
    
    def get_all_ec2_instances(self):
        print (self.application)
