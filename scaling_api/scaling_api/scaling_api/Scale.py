from scaling_api import LaunchConfiguration, Asg , HealthCheckLB
import boto3


class ScaleEnvironment:

    def __init__(self,application,ec2client,elbclient,asgclient):
        self.application = application
        self.ec2client = ec2client
        self.elbclient = elbclient
        self.asgclient = asgclient
        self.scaling_type = None

    def UpdateDesiredInstanceCountForScaleUp(self,LiveAsg):
        LiveCount = int(LiveAsg.DesiredCount)
        temp = LiveCount + int(self.application.DesiredCount)
        self.application.CountToIncrease = LiveCount + temp


    def UpdateDesiredInstanceCountForScaleDown(self,LiveAsg):
        LiveCount = int(LiveAsg.DesiredCount)
        self.application.CountToIncrease = LiveCount + int(self.application.DesiredCount)

    def CheckForLaunchConfigurationUpdation(self,NewLcConfig,ExistingLcConfig):
        if NewLcConfig == ExistingLcConfig:
            return True
        else:
            return False

    def ScaleUpEnvironment(self):
        try:
            LoadBalacerObject = HealthCheckLB.LoadBalancer(self.elbclient)
            AsgObject = Asg.AutoScalingGroup(self.asgclient,self.application.ApplicationName)
            LiveAsg = AsgObject.GetLiveAutoscalingGroup()
            LCobject = LaunchConfiguration.LaunchConfig(self.asgclient,LiveAsg.LaunchConfig)
            LiveLc = LCobject.GetLiveLC()
            result = self.CheckForLaunchConfigurationUpdation(self.application.InstanceType,LiveLc.InstanceType)
            print (LiveAsg.AsgName)
            if result:
                LiveAsg.UpdateASGLaunchConfiguration(self.application,LiveLc.lcname,False)
                LoadBalacerObject.CheckInstanceHealth(LiveAsg.LoadBalancer)
            else:
                self.UpdateDesiredInstanceCountForScaleUp(LiveAsg)
                result = LCobject.CheckForExistingLC(LiveAsg.LaunchConfig,"ScaleUp",self.application.InstanceType)
                print (result)
                if result == False:
                    NewLaunchConfig = LCobject.CopyLaunchConfiguration(LiveLc,self.application)
                    LiveAsg.UpdateASGLaunchConfiguration(self.application,NewLaunchConfig,True)
                else:
                    LiveAsg.UpdateASGLaunchConfiguration(self.application,result,True)
                LoadBalacerObject.CheckInstanceHealth(LiveAsg.LoadBalancer)
                LiveAsg.ShrinkASGCluster(self.application)
            return True
        except:
            return False

    def ScaleDownEnvironment(self):
        try:
            LoadBalacerObject = HealthCheckLB.LoadBalancer(self.elbclient)
            AsgObject = Asg.AutoScalingGroup(self.asgclient,self.application.ApplicationName)
            LiveAsg = AsgObject.GetLiveAutoscalingGroup()
            LCobject = LaunchConfiguration.LaunchConfig(self.asgclient,LiveAsg.LaunchConfig)
            LiveLc = LCobject.GetLiveLC()
            result = self.CheckForLaunchConfigurationUpdation(self.application.InstanceType,LiveLc.InstanceType)
            if result:
                LiveAsg.ShrinkASGCluster(self.application)
                LoadBalacerObject.CheckInstanceHealth(LiveAsg.LoadBalancer)
            else:
                self.UpdateDesiredInstanceCountForScaleDown(LiveAsg)
                result = LCobject.CheckForExistingLC(LiveAsg.LaunchConfig,"ScaleDown",self.application.InstanceType)
                print (result)
                if result == False:
                    NewLaunchConfig = LCobject.CopyLaunchConfiguration(LiveLc,self.application)
                    LiveAsg.UpdateASGLaunchConfiguration(self.application,NewLaunchConfig,True)
                else:
                    LiveAsg.UpdateASGLaunchConfiguration(self.application,result,True)
                LoadBalacerObject.CheckInstanceHealth(LiveAsg.LoadBalancer)
                LiveAsg.ShrinkASGCluster(self.application)
            return True
        except:
            return False

            