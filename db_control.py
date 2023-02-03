import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()
cur.execute(""" SELECT MAX(days) FROM USD_RUB_data""")
row = cur.fetchall()
print(row)
cur.execute(f"""DELETE FROM USD_RUB_data WHERE days = '{row[0][0]}'""")

cur.execute(""" SELECT MAX(days) FROM USD_RUB_data""")
row = cur.fetchall()
print(row)
con.commit()
cur.close()