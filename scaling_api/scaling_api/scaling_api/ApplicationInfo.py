

class Application:

    def __init__(self):
        self.ApplicationName = None
        self.InstanceType = None
        self.DesiredCount = None
        self.MaxCount = None
        self.MinCount = None
        self.CountToIncrease = None

    def getApplicationName(self):
        return self.ApplicationName

    def setApplicationName(self, value):
        self.ApplicationName = value

    def getInstanceType(self):
        return self.InstanceType

    def setInstanceType(self, value):
        self.InstanceType = value

