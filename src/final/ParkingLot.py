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
    set_display() # 전광판에 층마다 남은 자리 띄우기
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

            #print(row[0])

        self.__pksp_list = [ParkingSpot(pksp_list[i], db_path)
                            for i in range(len(pksp_list))]

    def set_display(self):
        self.mypmsdb.cur.execute('SELECT Parking_status FROM PARKINGLOT_LIST')
        pklt = []
        for row in self.mypmsdb.cur:
            if (row[0] == 0):
                pklt.append(1)
            else:
                pklt.append(0)
        empty= [[sum(pklt[:100])], [sum(pklt[100:200])], [sum(pklt[200:300])]]
        return empty

    def display(self):
        empty = self.set_display()
        print("#### 주차장 빈 자리 수 ####")
        print("지하 1층 : ", empty[0])
        print("지하 2층 : ", empty[1])
        print("지하 3층 : ", empty[2])


    @property
    def pksp_list(self):
        return self.__pksp_list
