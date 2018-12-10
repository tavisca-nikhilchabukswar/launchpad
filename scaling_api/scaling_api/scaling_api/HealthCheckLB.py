import sys
class LoadBalancer:

    def __init__(self,client):
        self.client = client

    def CheckInstanceHealth(self,LBName):
        try:
            waiter = self.client.get_waiter('instance_in_service')
            waiter.wait(
                LoadBalancerName=LBName,
                WaiterConfig={
                    'Delay': 20,
                    'MaxAttempts': 70
                }
            )
            print("All instances are in Inservice state !!!")
        except:
            print ("Unexpected error:", sys.exc_info())
            print ("Error in LoadBalancer HealthCheck !!!")
            sys.exit(-1)