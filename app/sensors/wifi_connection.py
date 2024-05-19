import socket
import network
import time
from machine import Pin, ADC
from sensor_config import *


class Connection:

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
    #    self.led = Pin("LED", Pin.OUT)
    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(WIFI_SSID, WIFI_PW)

    def show_connection_status(self):
        if self.wlan.isconnected() and self.wlan.status() >= 0:
            print("Connected")
            return 1
        else:
            return 0
    # def is_connection_aborted(self):
    #     self.led.value(0)
    #     reconnect_attempts = 0
    #     while not self.wlan.isconnected() or reconnect_attempts < 4:
    #         print("Lost Connection")
    #         print('Waiting for connection...')
    #         time.sleep(5)
    #         reconnect_attempts += 1
    #         break
    #     self.led.value(1)
    #     return True




