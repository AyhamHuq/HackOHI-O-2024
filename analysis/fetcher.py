import sqlite3
import os
import sys
from collections import namedtuple

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../processing'))

from sql import sql

data = namedtuple('data', ['pk1', 'pk2', 'text'])

class fetcher:
    def get_descriptions() -> list[data]:
        l = []

        con = sqlite3.connect(sql.db_name)
        cursor = con.cursor()

        cursor.execute(sql.retrieve_sql)

        for row in cursor.fetchall():
            (
                observation_no, 
                _, 
                point_name, 
                qualifier_text, 
                risk_notes, 
                risk_follow_up
            ) = row

            l.append(data(observation_no, point_name, ' '.join([
                point_name, 
                qualifier_text, 
                risk_notes, 
                risk_follow_up or ''
            ])))

        return l