
class BedRecord:
    def __init__(self, bedID, bedLabel="",patient=None,station=""):
        self.bedID = bedID
        self.bedLabel = bedLabel
        self.patient  = patient
        self.station  = station

