import sqlite3
from datetime import datetime, date
import string
import random
import time
# SQLite DB 연결

class DBinit:
    '''
    # Opens a connection to the SQLite database file database.
    conn : sqlite3.connect
    # A Cursor instance from sqlite3 class
    cur : sqlite3.connect.cursor
    --------------------------
    init_parkinglot_list(self) # Create parkinglot_list Table
    init_customer_list(self) # Create customer_list Table
    init_park_pay(self) # Create park_pay Table
    init_shopping_pay(self) # Create shopping_pay Table
    init_price(self) # Create price Table
    init_discount(self) # Create discount Table
    create_all(self) # Create all of tables above

    # Create random date between start and end.
    randomDate(self, start, end, prop, format = '%Y-%m-%d')
    # Create random time between start and end.
    randomTime(self, start, end, prop, format = '%H:%M:%S')
    # Calculate park_free_hour.
    cal_freeh(self, spay_amount, discount_list)
    # Calculate park_pay_amount.
    cal_price(self, minutes, price_list, free_hour)
    # Get the difference between start time and end time and return it as minute format
    diff_min(self, start, end, format)
    # Get the last id from certain table
    get_last_id(self, table, table_id)
    # print tables
    print_table(self, tbl_name)

    # Make tuples of PARKINGLOT_LIST and insert them
    mk_sample_parkinglot_list(self)
    # Make random sample tuples of CUSTOMER_LIST and insert them
    mk_mk_sample_cust(self, cust_num)
    # Make sample tuples of SHOPPING_PAY and insert them to SHOPPING_PAY
    mk_sample_spay(self, spay_num, start_date, end_date)
    # Make tuples of PRICE and insert them
    mk_sample_price(self, unit_minute, unit_price)
    # Make tuples of DISCOUNT and insert them
    mk_sample_discount(self, shopping_pay_minimum)
    # Make sample tuples of PARK_PAY and insert them
    mk_sample_ppay(self, range_list)
    # Make sample spay, ppay in certain period
    mk_sample_spay_ppay(self, start_y, end_y, cust)
    '''
    random.seed(0)

    def __init__(self,filename):
        print("DBinit 객체가 생성되었습니다.")

        # SQLite DB 연결
        # filename db가 있으면 연결, 없으면 새로 생성
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


    ##### 다른 함수 안에서 쓰이는 함수들 ####
    def randomDate(self, start, end, prop, format = '%Y-%m-%d'):
        """
        Create random date between start and end.
        """
        sdate = time.mktime(time.strptime(start, format))
        edate = time.mktime(time.strptime(end, format))
        pdate = sdate + prop * (edate - sdate)

        return time.strftime(format, time.localtime(pdate))


    def randomTime(self, start, end, prop, format = '%H:%M:%S'):
        """
        Create random time between start and end.
        """
        start_dt = '2018-01-01 ' + start
        end_dt = '2018-01-01 ' + end
        stime = time.mktime(time.strptime(start_dt, '%Y-%m-%d %H:%M:%S'))
        etime = time.mktime(time.strptime(end_dt, '%Y-%m-%d %H:%M:%S'))
        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))


    def cal_freeh(self, spay_amount, discount_list) :
        '''
        Calculate park_free_hour.
        Format of parameters
          spay_amount : int
          discount = list ['Shopping_pay_minimum', 'Free_hour']
        '''
        for i in range(len(discount_list)):
            if spay_amount < discount_list[i][0]:
                return discount_list[i][1]-1
        return discount_list[-1][1]


    def cal_price(self, minutes, price_list, free_hour):
        '''
        Calculate park_pay_amount.
        Format of parameters
          minutes : int
          price_list = [Unit_minute, Unit_price]
          free_hour = int
        '''
        free_min = free_hour * 60
        net_min = minutes - free_min
        if net_min <= 0:
            return 0

        t = int(net_min / price_list[0])
        if (net_min % price_list[0] == 0):
            return int(t * price_list[1])
        else:
            return int((t + 1) * price_list[1])


    def diff_min(self, start, end, format):
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))
        ptime = (etime - stime)
        return int(ptime/60)


    def get_last_id(self, table, table_id):
        self.cur.execute('SELECT '+table_id+' FROM ' + table + ' WHERE ' + table_id + ' = (SELECT MAX('+table_id+')  FROM '+table+')')
        last_id = self.cur.fetchone()
        return last_id[0]


    ##################################################################
    # print tables
    def print_table(self, tbl_name):
        # SQL 쿼리 실행은 cur.execute로 함
        self.cur.execute("select * from " + tbl_name)
        # 데이타 Fetch
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

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
                    +"-"+string.ascii_uppercase[zone]+str('{0:02d}'.format(spot))+"', 0, NULL)")

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
    # Make sample tuples of SHOPPING_PAY and insert them to SHOPPING_PAY
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
        open_time = "11:00:00"
        close_time = "23:00:00"
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
    # Make sample tuples of PARK_PAY and insert them to PARK_PAY
    ## PARK_PAY = {Ppay_id, Customer_car_num, Parking_spot, Park_in,
    ##             Park_out, Park_free_hour, Park_pay_amount, Park_is_paid}
    ## Ppay_id : 튜플 insert 시 자동으로 생성되는거라 얘를 빼고 나머지 컬럼값을 넣어줘야 함
    ## Customer_car_num 은 SHOPPING_PAY에서 전부 가져온다. 쇼핑한 사람은 모두 주차도 했다고 가정.
    ## Parking_spot PARKING_LOT 에서 가져온다고 가정. 둘 이상의 튜플이 같은시간대에 동일한 spot 을 가지면 안됨.
    ## Park_in 은 최소 오전 11시부터, SHOPPING_PAY 의 Shopping_pay_time 전까지
    ## Park_out 은 SHOPPING_PAY 의 Shopping_pay_time 이후부터 최대 오후 11시까지
    ## Park_free_hour 는 SHOPPING_PAY 의 Shopping_pay_amount 와 PRICE와 DISCOUNT 테이블에 근거하여 계산
    ## Park_free_hour 계산하는 모듈 따로 만들어야 함
    ## Park_is_paid 는 랜덤하게 0과 1 섞어서 넣어줌.
    def mk_sample_ppay(self, range_list):

        '''
        Make sample tuples of PARK_PAY and insert them to PARK_PAY
        PARK_PAY = {Ppay_id, Customer_car_num, Parking_spot, Park_in,
                    Park_out, Park_free_hour, Park_pay_amount, Park_is_paid}
        '''
        # Get Customer_car_num list which match the range of Spay_id from SHOPPING_PAY
        self.cur.execute("SELECT Customer_car_num FROM SHOPPING_PAY WHERE Spay_id >= ? AND Spay_id < ?",
                          (range_list[0],range_list[1]))
        cnum_list = []
        for row in self.cur:
            cnum_list.append(row[0])


        #### Parking_spot ####
        # Get Parking_spot list fom PARKINGLOT_LIST
        self.cur.execute('SELECT Parking_spot FROM PARKINGLOT_LIST')
        pksp_list = []
        for row in self.cur:
            pksp_list.append(row[0])


        #### Park_in & Park_out ####
        # Set opening hours
        open_time = "11:00:00"
        close_time = "23:00:00"

        # Get Shopping_pay_time list from SHOPPING_PAY
        self.cur.execute("SELECT Shopping_pay_time FROM SHOPPING_PAY WHERE Spay_id >= ? AND Spay_id < ?",
                          (range_list[0],range_list[1]))
        stime_list = []
        for row in self.cur:
            stime_list.append(row[0])

        # Set random park_in time between open_time and shopping_pay_time
        pin_list = []
        for stime in stime_list:
            # stime.split(' ')[0] = 'yyyy-mm-dd-yyyy'
            # ' '.join((stime.split(' ')[1:])) = 'hh:mm:ss'
            pin_list.append(stime.split(' ')[0] + ' ' + (self.randomTime(open_time, ' '.join((stime.split(' ')[1:])), random.random())))

        # Set random park_out time between shopping_pay_time and close_time
        pout_list = []
        for stime in stime_list:
            # stime.split(' ')[0] = 'yyyy-mm-dd-yyyy'
            # ' '.join((stime.split(' ')[1:])) = 'hh:mm:ss'
            pout_list.append(stime.split(' ')[0] + ' ' + (self.randomTime(' '.join((stime.split(' ')[1:])), close_time, random.random())))


        # Get parking minutes between park_in and park_out.
        # That is, "how long had this car parked?"
        pmin_list = []
        for i in range(len(pin_list)):
            pmin_list.append(self.diff_min(pin_list[i], pout_list[i], '%Y-%m-%d %H:%M:%S'))


        #### Park_free_hour ####
        # Get Shopping_pay_amount list from SHOPPING_PAY
        self.cur.execute("SELECT Shopping_pay_amount FROM SHOPPING_PAY WHERE Spay_id >= ? AND Spay_id < ?",
                          (range_list[0],range_list[1]))
        spay_list = []
        for row in self.cur:
            spay_list.append(row[0])

        # Get DISCOUNT table
        self.cur.execute('SELECT * FROM DISCOUNT')
        discount_list = []
        for row in self.cur:
            discount_list.append(list(row))

        # Calculate Park_free_hour
        pfrh_list = []
        for spay in spay_list:
            pfrh_list.append(self.cal_freeh(spay, discount_list))


        #### Park_pay_amount ####
        # Get PRICE table
        self.cur.execute('SELECT * FROM PRICE')
        for row in self.cur:
            price_list = list(row)

        # Calculate Park_pay_amount
        ppay_list = []
        for i in range(len(pmin_list)):
            ppay_list.append(self.cal_price(pmin_list[i], price_list, pfrh_list[i]))



        for i in range (len(cnum_list)):
            # 아래에서 주의해야 할 점
            # 변수가 text 여야 하면 (예; 차 번호), ",'" + 변수 + "'" 이렇게 넣어줘야 하고
            # 변수가 int 여야 하면 (예: 결제여부), "," + str(변수) 이렇게 넣어줘야 함
            self.cur.execute("""INSERT INTO PARK_PAY(Customer_car_num, Parking_spot, Park_in, Park_out,
                             Park_free_hour, Park_pay_amount, Park_is_paid) VALUES('"""
                            + cnum_list[i] + "', '" + pksp_list[i] + "', '" + pin_list[i] + "', '" + pout_list[i] + "', "
                            + str(pfrh_list[i]) + ", " + str(ppay_list[i]) + ", " + str(1) + ")")
        # commit 을 해줘야 sqlite 에 반영이 됨
        self.conn.commit()

    ##################################################################
    # Make sample spay, ppay in certain period
    def mk_sample_spay_ppay(self, start_y, end_y, cust):
        '''
        10일마다 약 cust명이 방문했다고 가정.
        range(start_y, end_y) 사이의 데이터 생성.
        '''
        for y in range(start_y, end_y):
            print(y, ' 년')
            for m in range(1, 13):
                print(m, ' 월')
                for i in range(2):
                    # Make Sample Shopping pay tuples (day 1~20)
                    self.mk_sample_spay(cust, str(y) + '-' + str(m) + '-' + str(1+i*10), str(y) + '-' + str(m) + '-' + str(10 + i*10))
                    # Make Park_pay Table
                    last = self.get_last_id('SHOPPING_PAY', 'Spay_id')
                    self.mk_sample_ppay([last - cust + 1, last + 1])

                # Case of the months with 31 days
                if m in {1, 3, 5, 7, 8, 10, 12} :
                    # Make Sample Shopping pay tuples (day 21~31)
                    self.mk_sample_spay(cust, str(y) + '-' + str(m) + '-' + str(21), str(y) + '-' + str(m) + '-' + str(31))
                    # Make Park_pay Table
                    last = self.get_last_id('SHOPPING_PAY', 'Spay_id')
                    self.mk_sample_ppay([last - cust + 1, last + 1])

                # Case of Feb
                elif m == 2 :
                    if y % 4 == 0:
                        # Make Sample Shopping pay tuples (day 21~29)
                        self.mk_sample_spay(cust, str(y) + '-' + str(m) + '-' + str(21), str(y) + '-' + str(m) + '-' + str(29))
                        # Make Park_pay Table
                        last = self.get_last_id('SHOPPING_PAY', 'Spay_id')
                        self.mk_sample_ppay([last - cust + 1, last + 1])

                    else:
                        # Make Sample Shopping pay tuples (day 21~28)
                        self.mk_sample_spay(cust, str(y) + '-' + str(m) + '-' + str(21), str(y) + '-' + str(m) + '-' + str(28))
                        # Make Park_pay Table
                        last = self.get_last_id('SHOPPING_PAY', 'Spay_id')
                        self.mk_sample_ppay([last - cust + 1, last + 1])

                # Case of the months with 30 days
                else :
                    # Make Sample Shopping pay tuples (day 21~30)
                    self.mk_sample_spay(cust, str(y) + '-' + str(m) + '-' + str(21), str(y) + '-' + str(m) + '-' + str(30))
                    # Make Park_pay Table
                    last = self.get_last_id('SHOPPING_PAY', 'Spay_id')
                    self.mk_sample_ppay([last - cust + 1, last + 1])
