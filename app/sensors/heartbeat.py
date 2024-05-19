import utime
from ntptime import *

class Heartbeat():

    def __init__(self):
        self.ntptime = Ntptime()

    # Check heartbeat every 5 mins
    def check_heartbeat(self, status):
        t = self.ntptime.time_getter()
        if t[4] % 5 == 0 and status == 0:
            print("Heartbeat_checked at", t)
            heartbeat = {"msg_type_cd": "H", "time": t}
            return 1, heartbeat

        elif t[4] % 5 == 0 and status != 0:
            return 1, {}

        elif t[4] % 5 != 0 and status == 0:
            return 0, {}

        elif t[4] % 5 != 0 and status != 0:
            return 0, {}

