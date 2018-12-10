import base64
import sys

class LaunchConfig:
    def __init__(self,client,lcname):
        self.client = client
        self.lcname = lcname
        self.ImageId = None
        self.KeyName = None
        self.SecurityGroup = None
        self.UserData = None
        self.InstanceType = None
        self.IamRole = None
        self.BlockDeviceMapping = None

    def GetDecodedUserData(self,UserData):
        return base64.b64decode(UserData)

    def CreateLCObject(self,lc):
        TempObj = LaunchConfig(self.client,self.lcname)
        TempObj.ImageId = lc.get("ImageId")
        TempObj.KeyName = lc.get("KeyName")
        TempObj.SecurityGroup = lc.get("SecurityGroups")
        TempObj.UserData = self.GetDecodedUserData(lc.get("UserData"))
        TempObj.InstanceType = lc.get("InstanceType")
        TempObj.IamRole = lc.get("IamInstanceProfile")
        TempObj.BlockDeviceMapping = lc.get("BlockDeviceMappings")
        return TempObj

    def GetLiveLC(self):
        try:
            response = self.client.describe_launch_configurations(LaunchConfigurationNames=[self.lcname])
            LcList = response.get("LaunchConfigurations")
            for lc in LcList:
                obj = self.CreateLCObject(lc)
                return obj
        except:
            print ("Unexpected error:", sys.exc_info())

    def CheckForHiephen(self,LcName):
        Temp = LcName.split('.')
        return Temp[0]

    def CopyLaunchConfiguration(self,OldLc,Application):
        try: 
            TempStr = str(Application.InstanceType).split('.')
            FinalStr= ''.join(TempStr)
            NewLCName = self.CheckForHiephen(OldLc.lcname)+"."+FinalStr
            response = self.client.create_launch_configuration(
                LaunchConfigurationName=NewLCName,
                ImageId=OldLc.ImageId,
                KeyName=OldLc.KeyName,
                SecurityGroups=OldLc.SecurityGroup,
                UserData=OldLc.UserData,
                InstanceType=Application.InstanceType,
                BlockDeviceMappings=OldLc.BlockDeviceMapping,
                IamInstanceProfile=OldLc.IamRole,
                EbsOptimized=False,
                InstanceMonitoring={
                    'Enabled': True|False
                }
            )
            return NewLCName
        except:
            print ("Unexpected error:", sys.exc_info())


    def CheckForExistingLC(self,lcname,type,instanceType):
        try:
            if type == "ScaleDown":        
                Name = lcname.split('.')
                response = self.client.describe_launch_configurations(LaunchConfigurationNames=[
                Name[0],
                ])
                if response.get('LaunchConfigurations'):
                    return Name[0]
                else:
                    return False
            elif type == "ScaleUp":
                Name = lcname.split('.')
                TempStr = str(instanceType).split('.')
                FinalStr= ''.join(TempStr)
                NewLCName = Name[0]+"."+FinalStr
                print (NewLCName)
                response = self.client.describe_launch_configurations(LaunchConfigurationNames=[
                NewLCName,
                ])
                if response.get('LaunchConfigurations'):
                    return NewLCName
                else:
                    return False
        except:
            print ("Not found")
            return False






