# 차단바 제어

import sqlite3
from Pms_db import DBinit
from Usonic import Usonic

class BlockBar:
    '''
    open : integer
    is_rgstrd : integer
    is_pssd : integer
    paid : integer
    dist : float
    WIDTH : float
    ----------------------
    is_registered(self, car_num) # 등록된 회원인지의 여부 반환
    is_paid(self, car_num) # 미납된 주차요금이 있는지 여부 반환
    blockbar_open(self, car_num) # 차단바를 연다.
    blockbar_close(self) # 차단바를 닫는다.
    is_passed(self) # 초음파 센서를 이용해 차량이 지나갔는지 여부 반환
    '''
    def __init__(self, db_path):
        print("BlockBarIn 객체가 생성되었습니다.")

        # SQLite DB 연결
        self.__mypmsdb = DBinit(db_path)
        self.__open = False  #초기 상태 = 차단바 closed
        self.__is_rgstrd = False  #초기 상태 = 회원이 아님
        self.__is_pssd = False  #초기 상태 = 차량이 아직 안 지나감
        self.__paid = False  #초기 상태 = 두번째 방문 차량에 해당됨
        self.__WIDTH = 200 # 입구의 너비. 입구에 차량이 없을 때 200cm
        self.__dist = self.__WIDTH # 물체와 초음파 센서 사이의 거리


    def is_registered(self, car_num):
        self.mypmsdb.cur.execute("select * from customer_list where customer_car_num = ?", (car_num,))
        cust_info = self.mypmsdb.cur.fetchone()
        print(cust_info)
        if (cust_info is not None):
            print("등록된 회원입니다.")
            self.is_rgstrd = True
            return self.is_rgstrd
        else:
            print("등록된 회원이 아닙니다.")



    def is_paid(self, car_num):
        self.paid = True
        self.mypmsdb.cur.execute("select Park_is_paid, Park_pay_amount from park_pay where customer_car_num = ?",
                     (car_num,))
        cust_info_two = self.mypmsdb.cur.fetchall()
        for i in range(len(cust_info_two)):
            if (cust_info_two[i][0] == 0):
                print("연체된 금액이 있습니다: ",cust_info_two[i][1],"원")
                self.paid = False

        # 미납요금 결제
        if(self.paid == False):
            self.pay(car_num)

        return self.paid



    # 미납요금 결제
    def pay(self, car_num):
        # 결제 모듈이 들어가야 함.
        # 결제 시스템과의 통합 필요.
        self.mypmsdb.cur.execute("""SELECT Park_is_paid, Park_pay_amount, Park_out
                                    FROM park_pay WHERE customer_car_num = ?""",
                                    (car_num,))
        cust_info = self.mypmsdb.cur.fetchall()

        # 미납요금에 대하여 결제
        for i in range(len(cust_info)):
            if (cust_info[i][0] == 0):
                self.mypmsdb.cur.execute("""UPDATE park_pay
                                            SET Park_is_paid = 1
                                            WHERE Park_out = ?""",
                                            (cust_info[i][2]))
                # commit 을 해줘야 sqlite 에 반영이 됨
                self.mypmsdb.conn.commit()
                print(cust_info[i][2], ' ', cust_info[i][1],
                ' 원에 대하여 결제가 완료되었습니다.')
                self.paid = True


# open은 is_registered와 paid 여부를 따져서 결정됨
    def blockbar_open(self, car_num):
        if (self.is_registered(car_num) == True):
            if (self.is_paid(car_num) == True):
                print("차단바가 열립니다.")
                self.open = True
            else:
                self.mypmsdb.cur.execute()
                print("미납요금이 결제됩니다.")
        else:
            self.open = False
            print("비회원에게 차단바를 열 수 없습니다.")


    def blockbar_close(self, t_pssd):
        if (self.is_passed(t_pssd) == True): #센서에서 차량이 지나갔다고 판단되면
            print("차단바가 닫힙니다.")
            self.open = False
        elif (self.is_passed(t_pssd) == False): # 아직 차량이 완전히 통과 못함
            print("빨리 지나가세요.")
            self.open = True


    def is_passed(self, t_pssd):
        if(t_pssd == True):
            self.__dist = Usonic.get_dist(198, 200)
            print(self.__dist)
            self.is_pssd = True
            return True
        if(t_pssd == False):
            self.__dist = Usonic.get_dist(10, 40)
            print(self.__dist)
            self.is_pssd = False
            return False
