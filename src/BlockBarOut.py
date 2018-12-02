# 차단바 제어 프로세스 중 출차 관련

import sqlite3
from WeightSensor import WeightSensor # 파일 이름 W_Sensor, 클래스 이름 w_sensor

class BlockBarOut:


    conn = sqlite3.connect("PMS_db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    def __init__(self, car_num):
        self.open = False  #초기 상태 = 차단바 is closed
        self.car_num = car_num  #이렇게 하는건지 모르겠음..
        self.is_pssd = False  #초기 상태 = 차단바 is opened/차량이 아직 안 지나감

    def open(self, is_paid):
        curs.execute("select * from park_pay where Park_is_paid = ?",
                     (self.paid,))
        cust_info = curs.fetchone()
        print(cust_info)
        if (cust_info_two is not None):
            print("차단바가 열립니다.")
            self.open = True
            return self.open
        else:
            print("차단바를 열 수 없습니다.")

    def close(self, is_pssd):
        if (w_sensor.pass = True): #pass가 명령어 같은데?!
            self.is_pssd = True
        if (self.is_pssd == True):
            print("차단바가 닫힙니다.")
            self.open = False
        else:
            print("빨리 지나가세요.")

    def getOpen(self):
        return self.open, self.car_num, self.is_pssd

    def setOpen(self, open):
        self.open = open
        self.car_num = car_num
        self.is_pssd = is_passd


conn.close()
