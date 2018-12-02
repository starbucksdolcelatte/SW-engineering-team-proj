# 차단바 제어 프로세스 중 입차 관련

import sqlite3
from WeightSensor import WeightSensor


class BlockBarIn:


    conn = sqlite3.connect("PMS_db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    def __init__(self, car_num):
        self.open = False  #초기 상태 = 차단바 closed
        self.is_rgstrd = False  #초기 상태 = 회원이 아님
        self.car_num = car_num
        self.is_pssd = False  #초기 상태 = 차량이 아직 안 지나감
        self.paid = False  #초기 상태 = 두번째 방문 차량에 해당됨

    def is_registered(self):
        curs.execute("select * from customer_list where customer_car_num = ?",
                     (self.car_num,))
        cust_info = curs.fetchone()
        print(cust_info)
        if (cust_info is not None):
            print("등록된 회원입니다.")
            self.is_rgstrd = True
            return self.is_rgstrd
        else:
            print("등록된 회원이 아닙니다.")

    def paid(self):
        curs.execute("select * from park_pay where Park_is_paid = ?",
                     (self.paid,))
        cust_info_two = curs.fetchone()
        print(cust_info_two)
        if (cust_info_two is not None):
            print("연체된 금액이 없습니다.")
            self.paid = True
            return self.paid
        else:
            print("연체된 금액이 있습니다.")

# open은 is_registered와 paid 여부를 따져서 결정됨
    def open(self, is_rgstrd, paid):
        if (self.is_rgstrd == True):
            if (self.paid == True):
                print("차단바가 열립니다.")
                self.open = True
            else:
                print("오늘은 결제하고 가셈.")
        else:
            print("차단바를 열 수 없습니다.")

    def close(self, is_pssd):
        if (w_sensor.is_passed = True): #센서에서 차량이 지나갔다고 판단되면
            self.is_pssd = True
        if (self.is_pssd == True):
            print("차단바가 닫힙니다.")
            self.open = False
        else:
            print("빨리 지나가세요.")

    def getOpen(self):
        return self.open, self.is_rgstrd, self.car_num, self.is_pssd, self.paid

    def setOpen(self, open):
        self.open = open
        self.is_rgstrd = is_rgstrd
        self.car_num = car_num
        self.is_pssd = is_pssd
        self.paid = paid


conn.close()
