from machine import Pin, ADC
import utime
import json
import socket

import wifi_connection
from sensor_config import *

# while True:
#     led = Pin("LED", Pin.OUT)
#     led.value(1)
#     pir = Pin(22, Pin.IN, Pin.PULL_DOWN).value()
#     print(pir)
#     led.value(0)
#     utime.sleep(1)
class Sensor():

    def __init__(self):

        self.litter_box_id = SENSORID[0]
        self.server_address = SERVERADDRESS
        self.wifi = None
        self.buffer_size = BUFFERSIZE
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = None
        self.threshold = THRESHOLD
        self.record_type = 1  # Assumed to be a normal enter got detected

    def execute(self):

        self.wifi = wifi_connection.Connection()
        self.wifi.connect()
        self.wifi.show_connection_status()

        while True:

            # if self.wifi.is_connection_aborted():
            #     print("Connection failed.")
            #     break

            sensor = Pin(22, Pin.IN, Pin.PULL_DOWN).value()

            if sensor > 0:
                self.timer = 0
                in_time = utime.localtime()
                print(in_time)

                while sensor != 0:
                    utime.sleep(1)
                    self.timer += 1

                    sensor = Pin(22, Pin.IN, Pin.PULL_DOWN).value()

                    if self.timer == self.threshold:
                        self.record_type = 2  # When it takes way too long for a cat to poop
                        break

                out_time = utime.localtime()
                print(out_time)

                record = {'in_time': in_time, 'out_time': out_time,
                          'litter_box_id': self.litter_box_id, 'type': self.record_type}

                try:
                    msg = json.dumps(record).encode('utf-8')
                    self.udp_client.sendto(msg, self.server_address)
                    print("Message Sent")
                except Exception as e:
                    print(e)
            else:
                pass