import numpy as np
import pandas as pd
import psycopg2
from sklearn.datasets import load_boston
from ddlgenerator.ddlgenerator import Table

# load boston data
data = load_boston()
df = pd.DataFrame(data.data, columns=data.feature_names)
df.head()

# connect to postgres and insert data
conn = psycopg2.connect(host="localhost", port = 5432, user="postgres", password="password")

df.to_csv('data.csv',index=False)

table = Table('data.csv', table_name='BOSTON_DATA')
sql = table.sql('postgresql', inserts=True)


cur = conn.cursor()
cur.execute(sql)
conn.commit()
cur.close()
conn.close()


# test to see if data inserted

conn = psycopg2.connect(host="localhost", port = 5432, user="postgres", password="password")

cur = conn.cursor()
cur.execute('''
SELECT CRIM
from BOSTON_DATA
limit 10
''')

print(cur.fetchall())
cur.close()

