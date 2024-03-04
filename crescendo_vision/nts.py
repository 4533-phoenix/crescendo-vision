from networktables import NetworkTables
import networktables
import socket

class NT:
    nt: NetworkTables

    def __init__(self):
        NetworkTables.initialize(server = "10.45.33.2")
        self.nt = NetworkTables.getTable(socket.gethostname())
    
    def putData(self, kind: str, data):
        self.nt.putValue(kind, data)

    def getValue(self, kind: str):
        self.nt.getValue(kind, defaultValue='')


    
