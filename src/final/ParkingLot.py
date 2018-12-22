import sqlite3
import time
from Pms_db import DBinit
from ParkingSpot import ParkingSpot


class ParkingLot:
    '''
    pksp_list : list of ParkingSpot() instances
    mypmsdb = DBinit() instance


    ----------------------
    get+위 모든 data fields
    set+위 모든 data fields
    get_usonic() # 초음파 센서가 측정한 거리 리턴
    get_status() # 초음파 센서가 측정한 거리를 처리(분석)하여 주차칸 상태 리턴
    set_led() # LED의 색상 변경 후 수정

    update_pklt_list(self) # db의 PARKINGLOT_LIST 테이블에 UPDATE
    '''

    def __init__(self, db_path):
        print("ParkingLot 객체가 생성되었습니다.")

        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)

        #### Parking_spot ####
        # Get Parking_spot list fom PARKINGLOT_LIST
        self.mypmsdb.cur.execute('SELECT Parking_spot FROM PARKINGLOT_LIST')
        pksp_list = []
        for row in self.mypmsdb.cur:
            pksp_list.append(row[0])
            print(row[0])

        self.__pksp_list = [[[ParkingSpot(pksp_list[l*100 + j*10 + i],db_path) for i in range(10)] for j in range(10)] for l in range(3)]


    @property
    def pksp_list(self):
        return self.__pksp_list
