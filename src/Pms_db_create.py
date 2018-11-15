import sqlite3
from datetime import datetime, date

# SQLite DB 연결
# test.db가 있으면 연결, 없으면 새로 생성
conn = sqlite3.connect("PMS_db.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

# Connection 으로부터 Cursor 생성
cur = conn.cursor()
# Create
# Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
cur.execute("""
    CREATE TABLE PARKINGLOT_LIST (
	Parking_spot TEXT PRIMARY KEY,
	Parking_status integer NOT NULL,
	Customer_car_num TEXT,
    FOREIGN KEY (Customer_car_num) REFERENCES CUSTOMER_LIST(Customer_car_num)
    )""")

cur.execute("""
    CREATE TABLE CUSTOMER_LIST (
	Customer_car_num TEXT PRIMARY KEY,
	Customer_card_info text NOT NULL,
	Customer_name TEXT,
    Customer_phone text)""")

# Park_is_paid : 0 is false(N), 1 is true(Y)
cur.execute("""
    CREATE TABLE PARK_PAY (
	Customer_car_num TEXT,
	Parking_spot TEXT,
    Park_in timestamp,
    Park_out timestamp,
    Park_free_hour integer NOT NULL,
	Park_pay_amount integer NOT NULL,
    Park_is_paid integer,
    FOREIGN KEY (Customer_car_num) REFERENCES CUSTOMER_LIST(Customer_car_num),
    FOREIGN KEY (Parking_spot) REFERENCES PARKINGLOT_LIST(Parking_spot)
    )""")

cur.execute("""
    CREATE TABLE SHOPPING_PAY (
	Customer_phone text,
	Shopping_pay_amount integer NOT NULL,
	Shopping_pay_time timestamp,
    FOREIGN KEY (Customer_phone) REFERENCES CUSTOMER_LIST(Customer_phone))""")

cur.execute("""
    CREATE TABLE PRICE (
	Unit_minute integer,
	Unit_price integer)""")

cur.execute("""
    CREATE TABLE DISCOUNT (
	Shopping_pay_minimum integer,
	Free_hour integer)""")

# Connection 닫기
conn.close()
