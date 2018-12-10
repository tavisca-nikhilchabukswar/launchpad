import boto3
import re
import sys
import time

class AutoScalingGroup:
    
    def __init__(self,client,application):
        self.client = client
        self.application = application
        self.AsgName = None
        self.LaunchConfig = None
        self.MinCount = None
        self.MaxCount = None
        self.DesiredCount = None
        self.LoadBalancer = None

    def MatchWithPattern(self,AppName,AsgName):
        pattern = re.compile(AppName+"*",re.IGNORECASE)
        result = pattern.match(AsgName)
        if result:
            return True
        else:
            return False

    def CreateASGObject(self,asg):
        self.AsgName = asg.get("AutoScalingGroupName")
        self.LaunchConfig = asg.get("LaunchConfigurationName")
        self.MinCount = asg.get("MinSize")
        self.MaxCount = asg.get("MaxSize")
        self.DesiredCount = asg.get("DesiredCapacity")
        LoadBalancers = asg.get("LoadBalancerNames")
        self.LoadBalancer = LoadBalancers[0]

    def GetLiveAutoscalingGroup(self):
        try:
            response = self.client.describe_auto_scaling_groups(MaxRecords=100)
            AsgList = response.get("AutoScalingGroups")
            for asg in AsgList:
                if self.MatchWithPattern(self.application,asg.get("AutoScalingGroupName")):
                    if int(asg.get("MinSize")) > 0 and int(asg.get("MaxSize")) > 0:
                        self.CreateASGObject(asg)
                        return self
        except:
            print ("Unexpected error:", sys.exc_info())


    def UpdateASGLaunchConfiguration(self,Application,LCName,flag):
        if flag == True:
            DesiredCount = Application.CountToIncrease
            MinCount = Application.CountToIncrease
        else:
            DesiredCount = Application.DesiredCount 
            MinCount = Application.DesiredCount     
        try:
            self.client.update_auto_scaling_group(
                AutoScalingGroupName=self.AsgName,
                LaunchConfigurationName=LCName,
                MinSize=int(MinCount),
                MaxSize=int(Application.MaxCount),
                DesiredCapacity=int(DesiredCount)
            )
            time.sleep(100)
            print("ASG Updated Successfully")
        except:
            print ("Unexpected error:", sys.exc_info())
            print ("Error While Updating ASG")
            sys.exit(-1)

    def ShrinkASGCluster(self,Application):
        try:
            self.client.update_auto_scaling_group(
                AutoScalingGroupName=self.AsgName,
                MinSize=int(Application.MinCount),
                MaxSize=int(Application.MaxCount),
                DesiredCapacity=int(Application.DesiredCount)
            )
            time.sleep(60)
            print("ASG Updated Successfully")
        except:
            print ("Unexpected error:", sys.exc_info())
            print ("Error While Updating ASG")
            sys.exit(-1)


        