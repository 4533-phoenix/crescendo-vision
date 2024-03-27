from networktables import NetworkTables, NetworkTable
import socket

class NT:
    nt: NetworkTable
    
    def __init__(self):
        NetworkTables.initialize(server = "10.45.33.2")
        self.nt = NetworkTables.getTable(socket.gethostname())

    def publishCamera():
        NetworkTables.getTable('CameraPublisher').getSubTable('note-detector').setDefaultValue('streams', ['mjpg:http://note-detector.local:1181/'])
    
    def putData(self, kind: str, data):
        self.nt.putValue(kind, data)

    def putBool(self, kind: str, val: bool):
        self.nt.putBoolean(kind, val)

    def putInt(self, kind: str, val: int):
        self.nt.putNumber(kind, val)

    def getValue(self, kind: str):
        self.nt.getValue(kind, defaultValue='')


    
