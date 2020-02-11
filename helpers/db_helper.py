import sqlite3
import pprint
import os
import datetime


class DbHelper:
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.db_path = os.path.join(basedir, 'dog_actions.db')
        # self.db_path = '../db/actions.sqlite'

    def determine_yesterday_morning(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        print(yesterday)
        print(str(yesterday))
        yesterday_morning = "00:00:00"
        return yesterday_morning

    def save_action(self, action, name, timestamp):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        params = (name, action, timestamp)
        print(params)
        sql = ''' INSERT INTO actions(name, action, timestamp) VALUES(?,?,?) '''
        res = cur.execute(sql, params)
        row = res.lastrowid
        conn.commit()
        conn.close()
        print("Row: " + str(row))
        return row

    def list_actions(self):
        conn = sqlite3.connect(self.db_path)
        # res = conn.execute("SELECT * FROM `actions`")
        yesterday_morning = self.determine_yesterday_morning()
        res = conn.execute("SELECT * FROM `actions` WHERE `timestamp` >= " + yesterday_morning)
        data = res.fetchall()
        pprint.pprint(data)
        return data
