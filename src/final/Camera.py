'''
cam_id : str
--------------------------------
recog_carnum(self): string

'''
import random
from datetime import datetime
from Pms_db import DBinit

class Camera:
    random.seed(datetime.now())

    def __init__(self, db_path, cam_id):
        #print(cam_id, " : Camera 객체가 생성되었습니다.")
        # Camera ID 설정
        self.__cam_id = cam_id
        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)


    def recog_carnum(self, is_registered, is_parked):
        # 실제 번호판 인식이 되어야 하지만, 구현하지 못했으므로
        # 랜덤 차량번호를 return 한다.
        # test를 위해, is_registered가 0이면 등록되지 않은 차량번호를 return,
        # is_registered == 1 이면 고객 테이블에 등록된 차량번호를 return
        # is_parked == 1 이면 PARKINGLOT_LIST 테이블에 등록된 차량번호를 return(출차)
        if (is_registered == 1):
            # Get CUSTOMER_LIST table
            self.mypmsdb.cur.execute('SELECT Customer_car_num FROM CUSTOMER_LIST')
            customer_list = []
            for row in self.mypmsdb.cur:
                customer_list.append(list(row)[0])
            #print(customer_list)

            # 주차장 안에 주차된 차량번호에 대하여,
            # Get PARKING_LOT table
            self.mypmsdb.cur.execute("""SELECT Customer_car_num
                FROM PARKINGLOT_LIST WHERE Parking_status = ?"""
                , (str(1),))
            pklt_list = []
            for row in self.mypmsdb.cur:
                pklt_list.append(list(row)[0])
            print(pklt_list)

            # 입차
            if(is_parked == 0):
                # 주차장 안에 있는 차량번호는 customer_list 에서 삭제
                for row in pklt_list:
                    if(row in customer_list):
                        #print('\n\n\n 있음 \n\n\n')
                        customer_list.remove(row)

                #print(customer_list)

                to = len(customer_list)
                index = random.randrange(0, to)
                print(index)
                return customer_list[index]

            # 출차
            elif(is_parked == 1):
                to = len(pklt_list)
                index = random.randrange(0, to)
                print(index)
                return pklt_list[index]


        elif (is_registered == 0):
            return "11기1111"

    @property
    def cam_id(self):
        return self.cam_id
