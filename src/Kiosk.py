import sqlite3


class Kiosk:

    """
    staff_tel:str
    car_num:str

    get_location(car_num:str):str
    get_car_num():car_num:str
    get_staff_tel():staff_tel:str
    set_car_num(str):none
    set_staff_tel(str):none
    """
    db_path = 'pms_db_fin_1.sqlite'
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    def __init__(self):
        self._staff_tel = '010-0000-0000'
        self._car_num = None

    def get_location(self, car_num):
        car_num = str(car_num)
        # 숫자로만 이루어졌는지 홖인
        if car_num.isdigit():
            # 4자리가 아니면
            if len(car_num) != 4:
                print("4자리의 차량번호 입력")
            else:
                self.cursor.execute("select PARKING_SPOT from PARKINGLOT_LIST where customer_car_num like ?",
                                    ('___' + car_num,))

                location = self.cursor.fetchone()
                # 잘못된 차랑번호입력 -> 쿼리결과 null
                if location is None:
                    print("차량번호를 다시 확인해주십시오.")
                    return
                else:  # location is not None
                    location = location[0]
                    print(car_num + "의 주차위치 : " + location)
                    return location
        # 숫자로만 이루어진 차량번호입력이 아니었을경우 ex) '가12'
        else:
                print("4자리의 차량번호 입력")


    @property
    def car_num(self):
        return self._car_num

    @car_num.setter
    def car_num(self, new_car_number):
        if not(len(new_car_number) == 4 and new_car_number.isdigit()):
            print("4자리의 차량번호 입력")
        else:
            self._car_num = new_car_number

    @property
    def staff_tel(self):
        return self._staff_tel

    @staff_tel.setter
    def staff_tel(self, telephone):
        # 정규표현식을 쓰고싶다
        # if telephone !=
        self._staff_tel = telephone
