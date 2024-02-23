from networktables import NetworkTables

class NT:
    def __init__(self):
        NetworkTables.initialize(server = "10.45.33.2")
        self.sd = NetworkTables.getTable("SmartDashboard")
    
    def putData(self, data):
        self.sd.putRaw("data", data)

    def getIt(self):
        return self.sd.getRaw("data", "apush")



    
