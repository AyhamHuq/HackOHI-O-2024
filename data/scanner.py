import sqlite3
import csv

from sql import sql

csv_name = 'input.csv'

con = sqlite3.connect(sql.db_name)
cursor = con.cursor()

cursor.execute(sql.create_sql)

# remove all data from table
cursor.execute(sql.delete_sql)

with open(csv_name, 'r') as input:
    reader = csv.reader(input)

    # skip first row (attribute headers)
    next(reader)

    for row in reader:
        (
            observation_no, 
            date, 
            point_name, 
            qualifier_text, 
            risk_notes, 
            risk_follow_up
        ) = row

        cursor.execute(sql.insert_sql, (
            int(observation_no), 
            date, 
            point_name, 
            qualifier_text, 
            risk_notes, 
            risk_follow_up if risk_follow_up else None
        ))

con.commit()
con.close()