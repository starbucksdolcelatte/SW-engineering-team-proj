import sqlite3
from datetime import datetime, date

# SQLite DB 연결
# test.db가 있으면 연결, 없으면 새로 생성
conn = sqlite3.connect("PMS_db.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# Insert
cur.execute("INSERT INTO PARKINGLOT_LIST VALUES('B1-A1', 0, '99구9999')")
# SQL 쿼리 실행
cur.execute("select * from PARKINGLOT_LIST")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()
