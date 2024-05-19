from machine import Pin, ADC
import utime
import json
import socket

import wifi_connection
from sensor_config import *
from ntptime import *
from heartbeat import *

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

        self.ntptime = Ntptime()
        self.board_led = Pin("LED", Pin.OUT)

        self.heartbeat = Heartbeat()

    def execute(self):

        self.board_led.value(1)  # power on sign
        utime.sleep(5)
        self.board_led.value(0)

        self.wifi = wifi_connection.Connection()
        self.wifi.connect()

        for c in range(5):  # wifi connecting sign
            self.board_led.value(0)
            utime.sleep(0.3)
            self.board_led.value(1)
            utime.sleep(0.3)
            c += 1

        utime.sleep(5)  # wait for wifi connection status to change
        wifi_status = self.wifi.show_connection_status()
        print(wifi_status)
        self.board_led.value(1 - wifi_status)

        heartbeat_check_status = 0
        while True:

            heartbeat_check_status, heartbeat_data = self.heartbeat.check_heartbeat(heartbeat_check_status)

            if heartbeat_data is None:
                continue
            else:
                try:
                    msg = json.dumps(heartbeat_data).encode('utf-8')
                    self.udp_client.sendto(msg, self.server_address)
                    print(msg)
                    print("Message Sent")
                except Exception as e:
                    print(e)

            # if self.wifi.is_connection_aborted():
            #     print("Connection failed.")
            #     break

            sensor = Pin(22, Pin.IN, Pin.PULL_DOWN).value()

            if sensor > 0:
                self.timer = 0
                # in_time = utime.localtime()
                in_time = self.ntptime.time_getter()
                print(in_time)

                while sensor != 0:
                    utime.sleep(1)
                    self.timer += 1

                    sensor = Pin(22, Pin.IN, Pin.PULL_DOWN).value()

                    if self.timer == self.threshold:
                        self.record_type = 2  # When it takes way too long for a cat to poop
                        break

                # out_time = utime.localtime()
                out_time = self.ntptime.time_getter()
                print(out_time)

                record = {'in_time': in_time, 'out_time': out_time, 'litter_box_id': self.litter_box_id,
                          'type': self.record_type, 'msg_type_cd': 'N'}
                try:
                    msg = json.dumps(record).encode('utf-8')
                    self.udp_client.sendto(msg, self.server_address)
                    print("Message Sent")
                except Exception as e:
                    print(e)
            else:
                continue