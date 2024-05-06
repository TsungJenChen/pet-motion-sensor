import datetime
import socket
import time
import ast
from .server_config import *
from db.postgres_client import PostgresSQL
from db.queries import *
#import boto3
import json
from .message import Message


class Server:

    def __init__(self):
        # Server config related
        self.buffer_size = BUFFERSIZE
        self.server_port = SERVERPORT
        self.server_ip = SERVERIP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # DB related
        self.db = PostgresSQL()

        # AWS related
        # self.lambda_client = boto3.client('lambda', region_name=None, api_version=None, use_ssl=True, verify=None,
        #                                   endpoint_url=None, aws_access_key_id=None, aws_secret_access_key=None,
        #                                   aws_session_token=None, config=None)

        # Local Virtual Machine testing

    def execute(self):

        self.server_socket.bind((self.server_ip, self.server_port))
        print("Server is Up and Listening")

        while True:
            self.litter_box_sensor()

    def litter_box_sensor(self):
        m, address = self.server_socket.recvfrom(self.buffer_size)

        data = ast.literal_eval(m.decode('utf-8'))

        in_and_out_record = self.data_formatter(data)

        self.db.add_record(SQL_DICT['INSERT_LITTERBOX_RECORD'], in_and_out_record)

        # self.invoke_lambda()

        print(data)  # Leave for logging

    @staticmethod
    def data_formatter(data: dict):
        in_time = datetime.datetime(*tuple(data["in_time"][0:6]))
        out_time = datetime.datetime(*tuple(data["out_time"][0:6]))
        record = {"in_time": in_time,
                  "out_time": out_time,
                  "duration": out_time - in_time,
                  "litter_box_id": data["litter_box_id"],
                  "record_type": data["type"],
                  "update_time": datetime.datetime.now(),
                  "update_user_id": "Sensor",
                  "create_time": datetime.datetime.now(),
                  "create_user_id": "Sensor"
                  }

        return record

    # def invoke_lambda(self, data: dict):
    #
    #     if data['type'] == 1:
    #         msg = Message.MSG['normal'].format(data['litter_box_id'], data['in_time'], data['out_time'])
    #     elif data['type'] == 2:
    #         msg = Message.MSG['abnormal'].format(data['litter_box_id'], data['in_time'], data['out_time'])
    #     else:
    #         pass
    #
    #     self.lambda_client.invoke(
    #         FunctionName='LAMBDA_FUNC_NAME',
    #         InvocationType='RequestResponse',
    #         LogType='None',  # 'Tail'
    #         ClientContext='string',
    #         Payload=json.dumps(msg),
    #         Qualifier='string'
    #     )

if __name__ == "__main__":

    Server().execute()