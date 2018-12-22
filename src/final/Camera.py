'''
cam_num : str

--------------------------------
proc_vrn(image): string
proc_zone_now(image): string list
proc_zone_status(DB): string list

get+위 모든 data fields
set+위 모든 data fields
'''
import random
from Pms_db import DBinit

class Camera:
    def __init__(self, db_path):
        print("Camera 객체가 생성되었습니다.")
        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)


    def recog(self):

        # Get CUSTOMER_LIST table
        self.mypmsdb.cur.execute('SELECT Customer_car_num FROM CUSTOMER_LIST')
        customer_list = []
        for row in self.mypmsdb.cur:
            customer_list.append(list(row))
        index = random.randrange(len(customer_list))

        return customer_list[index]
