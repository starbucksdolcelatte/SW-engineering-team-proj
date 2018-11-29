import sqlite3
import time

# SQLite DB 연결
# test.db가 있으면 연결, 없으면 새로 생성
con = sqlite3.connect("PMS_db_car.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

# Connection 으로부터 Cursor 생성
curs = con.cursor()


class Car:
    '''
    car_num : str
    location : str
    status : int
    in_time : str
    out_time : int

    ----------------------
    get+위 모든 data fields
    set+위 모든 data fields
    in()
    out()
    park()
    move()
    '''

    def __init__(self, car_num):
        print("Car 객체가 생성되었습니다.")
        self.__car_num = car_num
        print("Car number = " + self.__car_num)
        self.__location = ''
        self.__status = ''
        self.__in_time = ''
        self.__out_time = ''

    @property
    def car_num(self):
        return self.__car_num

    @property
    def location(self):
        return self.__location

    @property
    def status(self):
        return self.__status

    @property
    def in_time(self):
        return self.__in_time

    @property
    def out_time(self):
        return self.__out_time


    '''
    park()   칸에 주차하기
    move()   칸에서 차 빼기
    '''
    def park(self, parking_lot):
        now = time.localtime()
        self.__in_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.__location = parking_lot
        self.__status = 'parking'

        print("주차 시작시각 : " + self.__in_time)
        print("주차 칸 : " + self.__location)
        print("주차 상태 : " + self.__status)

    def move(self):
        now = time.localtime()
        self.__out_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.__status = 'moved'

        print("주차 종료시각 : " + self.__out_time)
        print("주차 칸 : " + self.__location)
        print("주차 상태 : " + self.__status)
