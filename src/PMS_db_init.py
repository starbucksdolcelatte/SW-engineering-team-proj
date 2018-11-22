import sqlite3
from datetime import datetime, date
import string

# SQLite DB 연결
# test.db가 있으면 연결, 없으면 새로 생성
conn = sqlite3.connect("PMS_db.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# Insert

## PARKINGLOT_LIST = {Parking_spot, Parking_status, Customer_car_num}
## Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
## Total 3 levels, A-J zones, 1-10 spots
## ['B3-J10', 0, NULL]
for floor in range (1,4):
    for i in range (0,10):
        for j in range (1,11):
            cur.execute("INSERT INTO PARKINGLOT_LIST VALUES('B"+str(floor)+"-"+string.ascii_uppercase[i]+str(j)+"', 0, NULL)")


# SQL 쿼리 실행
cur.execute("select * from PARKINGLOT_LIST")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()
