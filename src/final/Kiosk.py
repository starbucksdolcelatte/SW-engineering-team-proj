import sqlite3
from Pms_db import DBinit

class Kiosk:

    """
    staff_tel:str
    -----------------------------
    get_location(car_num:str):str
    get_staff_tel():staff_tel:str
    set_staff_tel(str):none
    """

    def __init__(self, db_path):
        self._staff_tel = '010-1234-2173'
        # SQLite DB 연결
        self.mypmsdb = DBinit(db_path)


    def get_location(self, car_num):
        car_num = str(car_num)
        # 숫자로만 이루어졌는지 홖인
        if car_num.isdigit():
            # 4자리가 아니면
            if len(car_num) != 4:
                print("4자리의 차량번호를 입력해주세요.")
            else:
                self.mypmsdb.cur.execute("select PARKING_SPOT from PARKINGLOT_LIST where customer_car_num like ?",
                                    ('___' + car_num,))
                location = self.mypmsdb.cur.fetchone()

                # 잘못된 차랑번호입력 -> 쿼리결과 null
                if location is None:
                    print("해당 차량이 존재하지 않습니다. 차량번호를 다시 확인해주십시오.")
                    return
                else:  # location is not None
                    location = location[0]
                    print(car_num + "의 주차위치 : " + location)
                    return location
        # 숫자로만 이루어진 차량번호입력이 아니었을경우 ex) '가12'
        else:
                print("4자리의 차량번호를 입력해주세요.")

    def get_staff_tel(self):
        print('안내원 번호는 ', self._staff_tel, '입니다 ^^')
        return self._staff_tel

    def set_staff_tel(self, telephone):
        # 정규표현식을 쓰고싶다
        self._staff_tel = telephone
