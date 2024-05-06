import unittest
import datetime
import db
from app import server
from db import postgres_client
from db.queries import *
from app.linebot import line_bot


class TestServer(unittest.TestCase):

    def test_linebot(self):
        LB = line_bot.LineBot()
        LB.send_message('The current time is ' + datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
    def test_aws(self):
        pass

    def test_db_add_record(self):

        test_record = {"in_time": '2024-03-31 18:00:00.000',
                       "out_time": '2024-03-31 18:10:00.000',
                       "duration": '10 min',
                       "pee_or_poop": '1',
                       "litter_box_id": 1,
                       "record_type": '1',
                       "notes": None,
                       "update_time": '2024-03-31 18:10:05.000',
                       "update_user_id": 'test',
                       "create_time": '2024-03-31 18:10:05.000',
                       "create_user_id": 'test'
                       }
        test_db = db.postgres_client.PostgresSQL()

        test_db.add_record(SQL_DICT['INSERT_LITTERBOX_RECORD'], test_record)

        expected = (datetime.datetime(2024, 3, 31, 18, 0, 0, 0), datetime.datetime(2024, 3, 31, 18, 10, 0, 0),
                    datetime.timedelta(minutes=10), '1', 1, '1', None, datetime.datetime(2024, 3, 31, 18, 10, 5, 0),
                    'test', datetime.datetime(2024, 3, 31, 18, 10, 5, 0), 'test')
        result = test_db.select_records(SQL_DICT['SELECT_TEST_RECORDS'])
        self.assertEqual(expected, result[0][1:])
        test_db.delete_records(SQL_DICT['DELETE_TEST_RECORDS'])
        result = test_db.select_records(SQL_DICT['SELECT_TEST_RECORDS'])
        self.assertTrue(len(result) == 0)






if __name__ == "__main__":
    unittest.main()