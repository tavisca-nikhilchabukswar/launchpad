import boto3
import time
import os
import base64
import sys

_clusterName = sys.argv[1]
_desiredCapacity = int(sys.argv[2])
_containerCount = int(sys.argv[3])



def CheckIfContainerHealthy(_cluster, _serviceNameList, _client):
    _waiter = _client.get_waiter('services_stable')
    _waiter.wait(
    cluster= _cluster,
    services= _serviceNameList
    )    


def GetListOfServices(_cluster, _client):

    response = _client.list_services(   
        cluster= _cluster
     )
    _serviceArnList= response.get('serviceArns')
    _serviceNameList = []
    for service_arn in _serviceArnList:
        _serviceName = service_arn.split('/')[1]
        _serviceNameList.append(_serviceName)
    return _serviceNameList

def UpdateAllServicesInCluster(_serviceNameList, _cluster, _ecsclient, _autoscalingclient):
    
    for _service in _serviceNameList:
        response = _autoscalingclient.register_scalable_target(
            MaxCapacity=5,
            MinCapacity= int(_containerCount),
            ResourceId='service/' + _cluster + '/' + _service,
            ScalableDimension='ecs:service:DesiredCount',
            ServiceNamespace='ecs' )

        _response = _ecsclient.update_service(
            cluster= _cluster,
            service= _service,
            desiredCount= int(_containerCount) )
        
    

def GetDesiredDictionary(_clusterName, client):
    
    asgName = ''
    
    response = client.describe_auto_scaling_groups()
    _allAutoscalingGroups = response['AutoScalingGroups']
    

    for AsgDictionary in _allAutoscalingGroups:
        ASGTagList = AsgDictionary.get('Tags')
        for AsgTag in ASGTagList:
            if AsgTag.get('Key') == "Cluster" and AsgTag.get('Value') == _clusterName:
                asgName =  AsgDictionary.get('AutoScalingGroupName')
            

    clusterdict = {
        "asg":  asgName, 
        "cluster": _clusterName
    }

    return clusterdict
        




def ScaleASG(client, _clusterName, _desiredCapacity ):
    _asgName = GetDesiredDictionary(_clusterName, client)["asg"]
    try:
        _response = client.update_auto_scaling_group(
        AutoScalingGroupName=_asgName  ,
        DesiredCapacity= int(_desiredCapacity),
        MinSize=int(_desiredCapacity),
        MaxSize=int(_desiredCapacity)+1
        )
        print("Done !!")
        time.sleep(60)
    except:
         print ("Unexpected error:", sys.exc_info())
         print ("Response is Null, Cannot find autoscaling group")


    

 
def CheckRegistredContainerInstanceCount(_resource, _autoscalingclient):
    try:
        _response = _resource.describe_clusters(
            clusters=[
                GetDesiredDictionary(_clusterName, _autoscalingclient)["cluster"] 
            ],    
        )
        
    except:
        print ("Unexpected error:", sys.exc_info()) 
        print ("Instances successfully added to the cluster")
    return int(_desiredCapacity)


def GetASGClient():
    _client = boto3.client('autoscaling', region_name='us-east-1')
    return _client

def GetECSClient():
    _client = boto3.client('ecs', region_name = 'us-east-1')
    return _client

def GetAppAutoscalingClient():
    _autoscalingclient = boto3.client('application-autoscaling', region_name = 'us-east-1')
    return _autoscalingclient


def main():
    _client = GetASGClient()
    ScaleASG(_client, _clusterName, _desiredCapacity)
    print ("Updating ASG success !!")
    _ecsClient = GetECSClient()
    _appautoscalingClient = GetAppAutoscalingClient()
    count = CheckRegistredContainerInstanceCount(_ecsClient, _client)  
    print (count)
    _cluster = GetDesiredDictionary(_clusterName, _client)["cluster"]
    _serviceNameList = GetListOfServices(_cluster, _ecsClient)
    UpdateAllServicesInCluster(_serviceNameList, _cluster, _ecsClient, _appautoscalingClient)
    print("Successfully Updated Services !!")
    CheckIfContainerHealthy(_cluster, _serviceNameList, _ecsClient)
    print("All containers are healthy")




if __name__ == '__main__':
    main()