import sqlite3
from datetime import datetime, date
import string
import random
import time
# SQLite DB 연결

class DBinit:
    random.seed(0)

    def __init__(self,filename):
        print("DBinit 객체가 생성되었습니다.")

        # SQLite DB 연결
        # test.db가 있으면 연결, 없으면 새로 생성
        self.conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES)
        # Connection 으로부터 Cursor 생성
        self.cur = self.conn.cursor()



    # Create Tables
    def init_parkinglot_list(self) :
        # Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
        self.cur.execute("""
            CREATE TABLE PARKINGLOT_LIST (
        	Parking_spot TEXT PRIMARY KEY,
        	Parking_status integer NOT NULL,
        	Customer_car_num TEXT,

            CONSTRAINT fk_Customer
            FOREIGN KEY (Customer_car_num)
            REFERENCES  CUSTOMER_LIST(Customer_car_num)
            ON DELETE NO ACTION ON UPDATE CASCADE
            )""")
        self.conn.commit()
        print('PARKINGLOT_LIST Table이 생성되었습니다.')


    def init_customer_list(self):
        self.cur.execute("""
            CREATE TABLE CUSTOMER_LIST (
        	Customer_car_num TEXT PRIMARY KEY,
        	Customer_card_info text NOT NULL,
        	Customer_name TEXT NOT NULL)""")
        self.conn.commit()
        print('CUSTOMER_LIST Table이 생성되었습니다.')


    def init_park_pay(self):
        # Park_is_paid : 0 is false(N), 1 is true(Y)
        self.cur.execute("""
            CREATE TABLE PARK_PAY (
            Ppay_id INTEGER PRIMARY KEY AUTOINCREMENT,
        	Customer_car_num TEXT NOT NULL,
        	Parking_spot TEXT NOT NULL,
            Park_in text NOT NULL,
            Park_out text NOT NULL,
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
        self.conn.commit()
        print('PARK_PAY Table이 생성되었습니다.')


    def init_shopping_pay(self):
        self.cur.execute("""
            CREATE TABLE SHOPPING_PAY (
            Spay_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_car_num text ,
        	Shopping_pay_amount integer NOT NULL DEFAULT 0,
        	Shopping_pay_time text ,

            CONSTRAINT fk_Customer
            FOREIGN KEY (Customer_car_num)
            REFERENCES  CUSTOMER_LIST(Customer_car_num)
            ON DELETE NO ACTION ON UPDATE CASCADE
            )""")
        self.conn.commit()
        print('SHOPPING_PAY Table이 생성되었습니다.')


    def init_price(self):
        self.cur.execute("""
            CREATE TABLE PRICE (
        	Unit_minute integer,
        	Unit_price integer)""")
        self.conn.commit()
        print('PRICE Table이 생성되었습니다.')

    def init_discount(self):
        self.cur.execute("""
            CREATE TABLE DISCOUNT (
        	Shopping_pay_minimum integer,
        	Free_hour integer)""")
        self.conn.commit()
        print('DISCOUNT Table이 생성되었습니다.')


    def create_all(self):
        self.init_parkinglot_list()
        self.init_customer_list()
        self.init_park_pay()
        self.init_shopping_pay()
        self.init_price()
        self.init_discount()


    def strDateProp(self, start, end, format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        sdate = time.mktime(time.strptime(start, format))
        edate = time.mktime(time.strptime(end, format))
        pdate = sdate + prop * (edate - sdate)

        return time.strftime(format, time.localtime(pdate))




    def strTimeProp(self, start, end, format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """
        start_dt = '1/1/2018 ' + start
        end_dt = '1/1/2018 ' + end
        stime = time.mktime(time.strptime(start_dt, '%m/%d/%Y %I:%M:%S %p'))
        etime = time.mktime(time.strptime(end_dt, '%m/%d/%Y %I:%M:%S %p'))
        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))




    def randomDate(self, start, end, prop):
        return self.strDateProp(start, end, '%Y-%m-%d', prop)


    def randomTime(self, start, end, prop):
        return self.strTimeProp(start, end, '%I:%M:%S %p', prop)


    ##################################################################
    ## PARKINGLOT_LIST = {Parking_spot, Parking_status, Customer_car_num}
    ## Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
    ## Total 3 levels, A-J zones, 1-10 spots
    ## ['B3-J10', 0, NULL]
    def mk_sample_parkinglot_list(self):
        for floor in range (1,4):
            for zone in range (0,10):
                for spot in range (1,11):
                    self.cur.execute("INSERT INTO PARKINGLOT_LIST VALUES('B"+str(floor)
                    +"-"+string.ascii_uppercase[zone]+str(spot)+"', 0, NULL)")

    ##################################################################
    ## CUSTOMER_LIST = {Customer_car_num, Customer_card_info, Customer_name}
    ## Make sample tuple of CUSTOMER_LIST and insert it to CUSTOMER_LIST
    ## CUSTOMER_LIST = { Customer_car_num, Customer_card_info, Customer_name }
    def mk_sample_cust(self, cust_num):
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

        for _ in range (cust_num):
            self.cur.execute("INSERT INTO CUSTOMER_LIST VALUES('"
            '{0:02d}'.format(random.randrange(100)) + h_plate[random.randrange(len(h_plate))] + '{0:04d}'.format(random.randrange(10000)) +
                "','" + card[random.randrange(len(card))] + " " + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) + "-" + '{0:04d}'.format(random.randrange(10000)) +
                "','" + n_first[random.randrange(len(n_first))] + " " + n_middle[random.randrange(len(n_middle))] + " " + n_last[random.randrange(len(n_last))] +
                "')")
        self.conn.commit()


    ##################################################################
    # Make sample tuple of SHOPPING_PAY and insert it to SHOPPING_PAY
    ## SHOPPING_PAY = {Spay_id, Customer_car_num, Shopping_pay_amount, Shopping_pay_time}
    def mk_sample_spay(self, spay_num, start_date, end_date):
        '''
        Make sample tuples of SHOPPING_PAY and insert them to SHOPPING_PAY
        SHOPPING_PAY = {Spay_id, Customer_car_num, Shopping_pay_amount, Shopping_pay_time}
        # Format of parameters
          spay_num : int, 만들고자 하는 데이터 수
          start_date, end_date : str'%Y-%m-%d' 기간
        '''
        # Get Customer_car_num list
        self.cur.execute('SELECT Customer_car_num FROM CUSTOMER_LIST')
        cnum_list = []
        for row in self.cur:
            cnum_list.append(row[0])
        open_time = "11:00:00 AM"
        close_time = "11:00:00 PM"
        for i in range (spay_num):
            self.cur.execute("INSERT INTO SHOPPING_PAY(Customer_car_num, Shopping_pay_amount, Shopping_pay_time) VALUES('"
                        + cnum_list[random.randrange(len(cnum_list))]
                        + "'," + str((random.randrange(100,30000))*10)
                        + ",'" + self.randomDate(start_date, end_date, random.random()) + ' '
                        + self.randomTime(open_time, close_time, random.random())+"')")
        self.conn.commit()


    ##################################################################
    ## PRICE = {Unit_minute, Unit_price}
    ## 10 분 당 500 원
    def mk_sample_price(self, unit_minute, unit_price):
        self.cur.execute("INSERT INTO PRICE VALUES(" + unit_minute + "," + unit_price + ")")
        self.conn.commit()

    ##################################################################
    ## DISCOUNT = {Shopping_pay_minimum, Free_hour}
    def mk_sample_discount(self, shopping_pay_minimum):
        for i in range(1,6):
            self.cur.execute("INSERT INTO DISCOUNT VALUES(" + str((i*2-1)*shopping_pay_minimum) + ", " + str(i) + ")")
        self.conn.commit()

    ##################################################################
    # print tables
    def print_table(self, tbl_name):
        # SQL 쿼리 실행은 cur.execute로 함
        self.cur.execute("select * from " + tbl_name)
        # 데이타 Fetch
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
