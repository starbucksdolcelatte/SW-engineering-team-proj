import sqlite3

# SQLite DB 연결
# test.db가 있으면 연결, 없으면 새로 생성
conn = sqlite3.connect("test.db")

# Connection 으로부터 Cursor 생성
cur = conn.cursor()
# Create
cur.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)")
# Insert
cur.execute("INSERT INTO kakao VALUES('16.06.03', 97000, 98600, 96900, 98000, 321405)")
# SQL 쿼리 실행
cur.execute("select * from kakao")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()
