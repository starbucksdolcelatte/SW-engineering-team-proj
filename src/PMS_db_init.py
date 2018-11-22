import sqlite3
from datetime import datetime, date
import string
import random

random.seed(0)

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
def init_parkinglot_list():
    for floor in range (1,4):
        for i in range (0,10):
            for j in range (1,11):
                cur.execute("INSERT INTO PARKINGLOT_LIST VALUES('B"+str(floor)+"-"+string.ascii_uppercase[i]+str(j)+"', 0, NULL)")
    return 0


## CUSTOMER_LIST = {Customer_car_num, Customer_card_info, Customer_name}
h_plate = ['가','나','다','라','마',
                 '거','너','더','러','머','버','서','어','저',
                 '고','노','도','로','모','보','소','오','조',
                 '구','누','두','루','무','부','수','우','주',
                 '아','바','사','자',
                 '배','하','허','호']

n_first = ['KIM','LEE', 'PARK', 'KONG', 'YOON', 'HYUN', 'KANG', 'JEONG', 'MOON', 'CHA', 'HAN', 'HWANG', 'HA']
n_middle = ['SEO', 'MOON', 'YOON', 'KYUNG', 'HYUN', 'MIN', 'SOO', 'EUN', 'SEONG', 'JI']
n_last = ['JOON', 'MI', 'AH', 'JOO', 'YEON', 'HYUK', 'SEOK','WOON']

card = ['VISA', 'MasterCard', 'Amex', 'BC', 'UnionPay','JCB']

def init_customer_list():
    for i in range (0,5):
        for j in range (0,9):
            cur.execute("INSERT INTO CUSTOMER_LIST VALUES('"
            + str(i) + str(j) + h_plate[random.randrange(len(h_plate))] + str(random.randrange(1000,9999)) +
            "','" + card[random.randrange(len(card))] + " " + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) +
            "','" + n_first[random.randrange(len(n_first))] + " " + n_middle[random.randrange(len(n_middle))] + " " + n_last[random.randrange(len(n_last))] +
            "')")
    return 0


## SHOPPING_PAY = {Spay_id, Customer_car_num, Shopping_pay_amount, Shopping_pay_time}
def init_shopping_pay():
    for i in range (0,50):
        for j in range (0,9):
            cur.execute("INSERT INTO SHOPPING_PAY VALUES('"
            + str(i) + str(j) + h_plate[random.randrange(len(h_plate))] + str(random.randrange(1000,9999)) +
            "','" + card[random.randrange(len(card))] + " " + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) + "-" + str(random.randrange(1000,9999)) +
            "','" + n_first[random.randrange(len(n_first))] + " " + n_middle[random.randrange(len(n_middle))] + " " + n_last[random.randrange(len(n_last))] +
            "')")
    return 0


# SQL 쿼리 실행
cur.execute("select * from PARKINGLOT_LIST")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()
