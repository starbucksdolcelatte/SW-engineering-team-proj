import sqlite3
import time
from Pms_db import DBinit
from Usonic import Usonic


class ParkingSpot:
    '''
    car_num : str
    spot : str
    status : integer
    led : str
    mypmsdb = DBinit() instance
    dist : float
    HEIGHT : float

    ----------------------
    get+위 모든 data fields
    set+위 모든 data fields
    get_usonic() # 초음파 센서가 측정한 거리 리턴
    get_status() # 초음파 센서가 측정한 거리를 처리(분석)하여 주차칸 상태 리턴
    set_led() # LED의 색상 변경

    update_pklt_list(self) # db의 PARKINGLOT_LIST 테이블에 UPDATE
    '''


    def __init__(self, spot, db_path):
        print("ParkingSpot 객체가 생성되었습니다.")
        self.__spot = spot # 'B1-A1'
        print("Parking Spot = " + self.__spot)

        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)

        self.__car_num = '' # 'B1-A1'
        self.__status = 0 # Parking_status : 0 == vacant ; 1 == occupied ; 2 == moving_out
        self.__HEIGHT = 300 # 천장부터 바닥까지 거리 : 300 cm
        self.__dist = self.__HEIGHT # 천장부터 물체까지의 거리
        self.__led = 'GREEN'


    @property
    def car_num(self):
        return self.__car_num

    @property
    def spot(self):
        return self.__spot

    @property
    def status(self):
        return self.__status

    @property
    def dist(self):
        return self.__dist

    @property
    def led(self):
        return self.__led

    # 차량번호 설정
    def set_car_num(self,car_num):
        self.__car_num = car_num


    # 초음파 센서가 측정한 거리를 처리(분석)하여 주차칸 상태 리턴
    # t_status는 테스트를 위한 param. t_status에 따라 리턴값 달라짐
    def get_status(self, t_status):
        # 1초 마다 한 번씩 천장과 물체와의 거리를 분석하여,
        # 이 칸의 상태를 알아낸다.
        # 테스트를 위해 5초 동안만 값을 받았다.
        dist_past = 0
        dist_now = 0

        # status : 0 == vacant ; 1 == occupied ; 2 == moving_out
        if(t_status == 0):
            fr = 295
            to = 300
        elif(t_status == 1):
            fr = 70
            to = 79
        elif(t_status == 2):
            fr = 80
            to = 200

        for i in range(5):
            dist_past = dist_now.copy()
            time.sleep(1)
            dist_now = Usonic.get_dist(fr, to)

            # 현재거리 - 과거거리 > 10cm 이고 80 <= 현재거리 <= 200이면 출차중
            if (dist_now - dist_past > 10 and dist_now >= 80 and dist_now <= 200):
                self.__status = 2
                self.set_led()

            else :
                # [천장~바닥 거리 - 15 <= 현재거리 <= 천장~바닥 거리] 이면 비어있음
                if(dist_now >= (self.__HEIGHT - 15) and dist_now <= self.__HEIGHT ):
                    self.__status = 0
                    self.__car_num = ''
                    self.set_led()

                # 나머지의 경우 주차중
                else:
                    self.__status = 1
                    self.set_led()

        print(self.__status)
        return self.__status

    # LED의 색상 변경
    def set_led(self):
        if (self.__status == 0) :
            self.__led = 'GREEN'
            print("빈 칸입니다.")
        elif (self.__status == 1) :
            self.__led = 'RED'
            print("주차중인 칸입니다.")
        elif (self.__status == 2) :
            self.__led = 'YELLOW'
            print("출차중인 칸입니다.")

        print(self.__led)

        return self.__led



    # db의 PARKINGLOT_LIST 테이블에 업데이트
    def update_pklt(self):
        # UPDATE table이름 SET 컬럼이름 = 변경된값 WHERE 특정튜플
        self.mypmsdb.cur.execute("UPDATE PARKINGLOT_LIST SET Parking_status = ?, Customer_car_num = ? WHERE Parking_spot = ?",
            (self.__status, self.__car_num, self.__spot,))

        # commit 을 해줘야 sqlite 에 반영이 됨
        self.mypmsdb.conn.commit()

        self.mypmsdb.cur.execute("SELECT * FROM PARKINGLOT_LIST WHERE Parking_spot = ?", (self.__spot,))
        print('아래 튜플이 PARKINGLOT_LIST 테이블에 UPDATE 되었습니다.')
        print(self.mypmsdb.cur.fetchone())
