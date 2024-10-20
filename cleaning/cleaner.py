import os
import sys
import sqlite3
from collections import defaultdict

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../processing"))
from sql import sql

con = sqlite3.connect(sql.db_name)
cursor = con.cursor()

# replace duplicate risk with most outstanding risk values
cursor.execute(sql.retrieve_for_duplicates_sql)

data = []
for t in cursor.fetchall():
    if not t[2]: break
    data.append(t)

groups = defaultdict(list)
for n, pk2, low, medium, high in data:
    groups[n].append((pk2, low, medium, high))

cleaned = []
for a, group in groups.items():
    if (len(group) == 1): continue

    absolute_min = min(min(l[1:]) for l in group)
    pk2, low, medium, high = next(l for l in group if absolute_min in l[1:])
    
    for pk2, _, _, _ in group:
        new_tuple = (a, pk2, low, medium, high)
        cleaned.append(new_tuple)

for pk1, pk2, low, medium, high in cleaned:
    cursor.execute(sql.update_risk_sql, (low, medium, high, pk1, pk2))


# generate columns for classifcation
categories = ['risk', 'observation', 'hazard']
for title in categories:
    sql.add_column(cursor, title, 'TEXT')

cursor.execute(sql.retrieve_results_sql)

data = []
for t in cursor.fetchall():
    if not t[3]: break
    data.append(t)

commands = [sql.update_column(c) for c in categories]

for l1, m1, h1, p2, d2, e2, t3, fi3, e3, fa3, pk1, pk2 in data:
    _, risk = min([(l1, 'Low'), (m1, 'Medium'), (h1, 'High')])
    cursor.execute(commands[0], (risk, pk1, pk2))

    _, observation = min([(p2, 'PPE'), (d2, 'Documentation'), (e2, 'Equipment')])
    cursor.execute(commands[1], (observation, pk1, pk2))

    _, hazard = min([(t3, 'Traffic'), (fi3, 'Fire'), (e3, 'Electrical'), (fa3, 'Fall')])
    cursor.execute(commands[2], (hazard, pk1, pk2))

con.commit()
con.close()