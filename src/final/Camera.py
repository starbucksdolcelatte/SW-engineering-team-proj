'''
cam_id : str
--------------------------------
recog_carnum(self): string

'''
import random
from Pms_db import DBinit

class Camera:
    def __init__(self, cam_id, db_path):
        print("Camera 객체가 생성되었습니다.")
        # Camera ID 설정
        self.cam_id = cam_id
        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)


    def recog_carnum(self, is_registered):
        # 실제 번호판 인식이 되어야 하지만, 구현하지 못했으므로
        # 랜덤 차량번호를 return 한다.
        # test를 위해, is_registered가 0이면 등록되지 않은 차량번호를 return,
        # is_registered가 1이면 고객 테이블에 등록된 차량번호를 return
        if (is_registered == 1):
            # Get CUSTOMER_LIST table
            self.mypmsdb.cur.execute('SELECT Customer_car_num FROM CUSTOMER_LIST')
            customer_list = []
            for row in self.mypmsdb.cur:
                customer_list.append(list(row))
            index = random.randrange(len(customer_list))
            return customer_list[index]
        elif (is_registered == 0):
            return "11기1111"

    @property
    def cam_id(self):
        return self.cam_id
