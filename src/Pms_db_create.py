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

    CONSTRAINT fk_Customer
    FOREIGN KEY (Customer_car_num)
    REFERENCES  CUSTOMER_LIST(Customer_car_num)
    ON DELETE NO ACTION ON UPDATE CASCADE
    )""")

cur.execute("""
    CREATE TABLE CUSTOMER_LIST (
	Customer_car_num TEXT PRIMARY KEY,
	Customer_card_info text NOT NULL,
	Customer_name TEXT NOT NULL)""")

# Park_is_paid : 0 is false(N), 1 is true(Y)
cur.execute("""
    CREATE TABLE PARK_PAY (
    Ppay_id inte PRIMARY KEY,
	Customer_car_num TEXT NOT NULL,
	Parking_spot TEXT NOT NULL,
    Park_in timestamp NOT NULL,
    Park_out timestamp NOT NULL,
    Park_free_hour integer NOT NULL DEFAULT 0,
	Park_pay_amount integer NOT NULL DEFAULT 0,
    Park_is_paid integer NOT NULL DEFAULT 0,

    CONSTRAINT fk_Parkinglot
    FOREIGN KEY (Parking_spot)
    REFERENCES  PARKINGLOT_LIST(Parking_spot)
    ON DELETE NO ACTION ON UPDATE CASCADE,

    CONSTRAINT fk_Customer
    FOREIGN KEY (Customer_car_num)
    REFERENCES  CUSTOMER_LIST(Customer_car_num)
    ON DELETE NO ACTION ON UPDATE CASCADE
    )""")

cur.execute("""
    CREATE TABLE SHOPPING_PAY (
    Spay_id inte PRIMARY KEY,
    Customer_car_num text ,
	Shopping_pay_amount integer NOT NULL DEFAULT 0,
	Shopping_pay_time timestamp ,

    CONSTRAINT fk_Customer
    FOREIGN KEY (Customer_car_num)
    REFERENCES  CUSTOMER_LIST(Customer_car_num)
    ON DELETE NO ACTION ON UPDATE CASCADE
    )""")

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
