import sqlite3
import time
from Pms_db import DBinit

class Car:
    '''
    car_num : str
    location : str
    in_time : str
    out_time : int
    free_hour : integer
    pay_amount : integer
    is_paid : integer
    ----------------------
    park(self, parking_lot) # 칸에 주차하기
    move(self) # 칸에서 차 빼기
    set_pay_amount(self) # 무료 주차 시간, 주차요금 구해 저장하기
    park_pay (self, car_num, successed) # 주차요금 결제
    insert_ppay(self) # db의 park_pay 테이블에 삽입
    '''

    def __init__(self, car_num, db_path):
        print("Car 객체가 생성되었습니다.")
        self.__car_num = car_num
        print("Car number = " + self.__car_num)

        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)

        self.__location = '' # 'B1-A1'
        self.__in_time = '' # format = yyyy-mm-dd
        self.__out_time = '' # format = yyyy-mm-dd
        self.__free_hour = 0
        self.__pay_amount = 0
        self.__is_paid = 0


    @property
    def car_num(self):
        return self.__car_num

    @property
    def location(self):
        return self.__location

    @property
    def in_time(self):
        return self.__in_time

    @property
    def out_time(self):
        return self.__out_time

    @property
    def free_hour(self):
        return self.__free_hour

    @property
    def pay_amount(self):
        return self.__pay_amount

    @property
    def is_paid(self):
        return self.__is_paid


    # park()   칸에 주차하기
    def park(self, parking_lot):
        now = time.localtime()
        self.__in_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.__location = parking_lot

        print("주차 시작시각 : " + self.__in_time)
        print("주차 칸 : " + self.__location)

        self.mypmsdb.cur.execute("""INSERT INTO PARK_PAY(Customer_car_num, Parking_spot, Park_in) VALUES('"""
                        + self.car_num + "', '" + self.location + "', '" + self.in_time  + "')")

        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()

        self.mypmsdb.cur.execute("SELECT * FROM PARK_PAY WHERE Customer_car_num = ? AND Park_in = ?",
                                    (self.car_num, self.in_time,))
        print('아래 튜플이 PARK_PAY 테이블에 INSERT 되었습니다.')
        print(self.mypmsdb.cur.fetchone())


    # move()   칸에서 차 빼기
    def move(self):
        self.set_spay(67500) # 67500원 결제

        now = time.localtime()
        self.__out_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+2, now.tm_min, now.tm_sec)

        self.mypmsdb.cur.execute("SELECT * FROM PARK_PAY WHERE Customer_car_num = ? AND Park_in like ?",
                                    (self.car_num, self.__out_time[:10] + '%',))
        row = self.mypmsdb.cur.fetchone()
        if(row is not None):
            row = list(row)
        print(row)
        self.__location = row[2]
        self.__in_time = row[3]

        print("주차 종료시각 : " + self.__out_time)
        print("주차 칸 : " + self.__location)

        self.mypmsdb.cur.execute("""UPDATE PARK_PAY SET Park_out = ?
                WHERE Customer_car_num = ? AND Park_in like ?""",
            (self.__out_time, self.__car_num, self.__out_time[:10] + '%',))
        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()

        # 주차요금 UPDATE
        self.set_pay_amount()

        # 확인
        self.mypmsdb.cur.execute("SELECT * FROM PARK_PAY WHERE Customer_car_num = ? AND Park_out = ?",
                                    (self.car_num, self.__out_time,))
        print('아래 튜플이 PARK_PAY 테이블에 UPDATE 되었습니다.')
        print(self.mypmsdb.cur.fetchone())


    def set_spay(self, spay_amount):
        now = time.localtime()
        spay_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour+2, now.tm_min-15, now.tm_sec)

        self.mypmsdb.cur.execute("""INSERT INTO
        SHOPPING_PAY(Customer_car_num, Shopping_pay_amount, Shopping_pay_time)
        VALUES('"""+ self.car_num + "'," + str(spay_amount) + ", '" + spay_time  + "')")
        self.mypmsdb.conn.commit()

        # 확인
        self.mypmsdb.cur.execute("SELECT * FROM SHOPPING_PAY WHERE Customer_car_num = ? AND Shopping_pay_time = ?",
                                    (self.car_num, spay_time,))
        print('아래 튜플이 SHOPPING_PAY 테이블에 INSERT 되었습니다.')
        print(self.mypmsdb.cur.fetchone())


    # set_pay_amount()   무료 주차 시간, 주차요금 구해 저장하기
    def set_pay_amount(self):
        # Get parking minutes between park_in and park_out.
        # That is, "how long had this car parked?"
        pmin = self.mypmsdb.diff_min(self.__in_time, self.__out_time, '%Y-%m-%d %H:%M:%S')
        print('parked minutes : ', pmin)
        #### Park_free_hour ####
        # Get Shopping_pay_amount from SHOPPING_PAY
        # 오늘 입차한 손님의 쇼핑 구매 금액 찾기
        self.mypmsdb.cur.execute("SELECT Shopping_pay_amount FROM SHOPPING_PAY WHERE Customer_car_num = ? AND Shopping_pay_time like ?",
                                    (self.__car_num, self.__out_time[:10] + "%",))
        row = self.mypmsdb.cur.fetchone()
        if(row is not None):
            spay = row[0]
        else:
            spay = 0
        print("Shopping pay amount : ", spay)

        # Get DISCOUNT table
        self.mypmsdb.cur.execute('SELECT * FROM DISCOUNT')
        discount_list = []
        for row in self.mypmsdb.cur:
            discount_list.append(list(row))
        print("DISCOUNT Table\n",discount_list)

        # Calculate Park_free_hour
        self.__free_hour = self.mypmsdb.cal_freeh(spay, discount_list)
        print('park free hour : ',self.__free_hour)

        #### Park_pay_amount ####
        # Get PRICE table
        self.mypmsdb.cur.execute('SELECT * FROM PRICE')
        for row in self.mypmsdb.cur:
            price_list = list(row)

        # Calculate Park_pay_amount
        self.__pay_amount = self.mypmsdb.cal_price(pmin, price_list, self.__free_hour)
        print('park pay amount : ', self.__pay_amount)

        # UPDATE Table
        self.mypmsdb.cur.execute("""UPDATE PARK_PAY SET Park_pay_amount = ?, Park_free_hour = ?
                WHERE Customer_car_num = ? AND Park_in like ?""",
            (self.__pay_amount, self.__free_hour, self.__car_num, self.__out_time[:10] + '%',))
        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()


    # 주차요금 결제
    def park_pay (self, car_num, successed):
        # 결제 모듈이 들어가야 함.
        # 결제 시스템과의 통합 필요.
        # 고객의 카드 정보 제공하면, 한도초과가 아니면 결제 정상적으로 완료하고, 한도초과이면 결제 실패
        now = time.localtime()
        now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        if(successed == True):
            self.__is_paid = 1 # True

        # for test : 한도초과일 경우
        elif(successed == False):
            self.__is_paid = 0 # False

        # UPDATE Table
        self.mypmsdb.cur.execute("""UPDATE PARK_PAY SET Park_is_paid = ?
                WHERE Customer_car_num = ? AND Park_out like ?""",
            (self.__is_paid, self.__car_num, now_time[:10] + '%',))
        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()
        if(successed == True):
            print('결제가 완료되었습니다.')
        elif(successed == False):
            print('결제에 실패하였습니다. 미납요금은 추후 청구됩니다.')


        # 확인
        self.mypmsdb.cur.execute("SELECT * FROM PARK_PAY WHERE Customer_car_num = ? AND Park_out like ?",
                                    (self.car_num, now_time[:10] + '%',))
        print('아래 튜플이 PARK_PAY 테이블에 UPDATE 되었습니다.')
        print(self.mypmsdb.cur.fetchone())




    # db의 park_pay 테이블에 삽입
    def insert_ppay(self):
        self.mypmsdb.cur.execute("""INSERT INTO PARK_PAY(Customer_car_num, Parking_spot, Park_in, Park_out,
                         Park_free_hour, Park_pay_amount, Park_is_paid) VALUES('"""
                        + self.car_num + "', '" + self.location + "', '" + self.in_time + "', '" + self.out_time + "', "
                        + str(self.free_hour) + ", " + str(self.pay_amount) + ", " + str(self.is_paid) + ")")

        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()

        print(self.__in_time.split(' ')[0])
        self.mypmsdb.cur.execute("SELECT * FROM PARK_PAY WHERE Customer_car_num = ? AND Park_in = ?",
                                    (self.car_num, self.in_time,))
        print('아래 튜플이 PARK_PAY 테이블에 INSERT 되었습니다.')
        print(self.mypmsdb.cur.fetchone())
