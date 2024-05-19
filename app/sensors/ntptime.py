# References:
## https://github.com/micropython/micropython-lib/blob/master/micropython/net/ntptime/ntptime.py
## https://ippei8jp.hatenablog.jp/entry/2017/08/18/135755

import utime

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct


class Ntptime():

    def __init__(self):
        self.local_time_calibrator = 9*60*60
    def time_getter(self):
        NTP_DELTA = 2208988800
        ntp_host = "ntp.nict.jp"

        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(ntp_host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        local_time = val - NTP_DELTA + self.local_time_calibrator

        return utime.gmtime(local_time)