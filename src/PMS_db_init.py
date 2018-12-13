# Created By Seoyoon Park

import sqlite3
from datetime import datetime, date
import string
import random

random.seed(0)

# Connect to SQLite DB
## if exist "PMS_db.sqlite" then connect
## if not exitst "PMS_db.sqlite" then create
conn = sqlite3.connect("PMS_db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

# Create cursor from DB Connection
cur = conn.cursor()



##################################################################
## PARKINGLOT_LIST = {Parking_spot, Parking_status, Customer_car_num}
## Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
## Total 3 levels, A-J zones, 1-10 spots
## ['B3-J10', 0, NULL]
def init_parkinglot_list():
    for floor in range (1,4):
        for zone in range (0,10):
            for spot in range (1,11):
                cur.execute("INSERT INTO PARKINGLOT_LIST VALUES('B"+str(floor)
                +"-"+string.ascii_uppercase[zone]+str(spot)+"', 0, NULL)")
    return 0





##################################################################
## CUSTOMER_LIST = {Customer_car_num, Customer_card_info, Customer_name}
h_plate = ['가','나','다','라','마',
                 '거','너','더','러','머','버','서','어','저',
                 '고','노','도','로','모','보','소','오','조',
                 '구','누','두','루','무','부','수','우','주',
                 '아','바','사','자',
                 '배','하','허','호']

n_first = ['KIM','LEE', 'PARK', 'KONG', 'YOON', 'HYUN', 'KANG',
            'JEONG', 'MOON', 'CHA', 'HAN', 'HWANG', 'HA']
n_middle = ['SEO', 'MOON', 'YOON', 'KYUNG', 'HYUN', 'MIN',
            'SOO', 'EUN', 'SEONG', 'JI']
n_last = ['JOON', 'MI', 'AH', 'JOO', 'YEON', 'HYUK', 'SEOK','WOON']

card = ['VISA', 'MasterCard', 'Amex', 'BC', 'UnionPay','JCB']


# Make sample tuple of CUSTOMER_LIST and insert it to CUSTOMER_LIST
## CUSTOMER_LIST = { Customer_car_num, Customer_card_info, Customer_name }
def mk_sample_cust(cust_num):
    for _ in range (cust_num):
        cur.execute("INSERT INTO CUSTOMER_LIST VALUES('"
        '{0:02d}'.format(random.randrange(100)) + h_plate[random.randrange(len(h_plate))] + '{0:04d}'.format(random.randrange(10000)) +
            "','" + card[random.randrange(len(card))] + " " + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) +
            "','" + n_first[random.randrange(len(n_first))] + " " + n_middle[random.randrange(len(n_middle))] + " " + n_last[random.randrange(len(n_last))] +
            "')")
    return 0




##################################################################
# Make sample tuple of SHOPPING_PAY and insert it to SHOPPING_PAY
## SHOPPING_PAY = {Spay_id, Customer_car_num, Shopping_pay_amount, Shopping_pay_time}
def mk_sample_spay(spay_num):
    for _ in range (spay_num):
        cur.execute("INSERT INTO SHOPPING_PAY VALUES('"
        '{0:02d}'.format(random.randrange(100)) + h_plate[random.randrange(len(h_plate))] + '{0:04d}'.format(random.randrange(10000)) +
            "','" + card[random.randrange(len(card))] + " " + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) +
            "','" + n_first[random.randrange(len(n_first))] + " " + n_middle[random.randrange(len(n_middle))] + " " + n_last[random.randrange(len(n_last))] +
            "')")
    return 0


#init_parkinglot_list()
#init_customer_list()

# test case : normal data
cur.execute("INSERT INTO CUSTOMER_LIST VALUES('12가1234','VISA 1234-1234-1234-1234', 'KIM MIN JI')")
print('SUCCESS 1')

# test case : abnormal data :: to test primary key collision
cur.execute("INSERT INTO CUSTOMER_LIST VALUES('12가1234','VISA 1234-1234-1234-1234', 'KIM MIN JI')")
print('SUCCESS 2')


# SQL 쿼리 실행은 cur.execute로 함
cur.execute("select * from CUSTOMER_LIST")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()
