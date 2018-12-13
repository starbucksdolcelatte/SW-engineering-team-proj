'''
    open: bool

    ---------------------------------
    open(is_rgstrd : bool):None
    is_registered(car_num:str) : bool
    close(is_pssd:bool):None
    get+위 모든 data fields
    set+위 모든 data fields

'''
# 차단바 제어 프로세스 중 출차 관련

from User import User
from WeightSensor import WeightSensor # 파일 이름 W_Sensor, 클래스 이름 w_sensor

class BlockBarOut:


    def __init__(self, car_num):
        self.open = False  #초기 상태 '차단바 closed'
        self.car_num = car_num  #이렇게 하는건지 모르겠음..
        self.is_pssd = False  #초기 상태 '차단바 opened/차량이 아직 안 지나감'

    def open(self, is_paid):
        if (User.is_paid_park == True):
            print("차단바가 열립니다.")
            self.open = True
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


# 차단바 제어 프로세스 중 입차 관련
# 문제: 데이터필드인 car_num은 어디서 오는가...

from User import User
from WeightSensor import WeightSensor

class BlockBarIn:


    def __init__(self, car_num):
        self.open = False  #초기 상태 '차단바 closed'
        self.is_rgstrd = False  #초기 상태 '회원이 아님'
        self.car_num = car_num  #이렇게 하는건지 모르겠음
        self.is_pssd = False  #초기 상태 '차량이 아직 안 지나감'

    def is_registered(self, car_num):
        if (self.car_num == User.car_num):
            print("등록된 회원입니다.")
            self.is_rgstrd = True
            return self.is_rgstrd
        else:
            print("등록된 회원이 아닙니다.")

    def open(self, is_rgstrd):
        if (self.is_rgstrd == True):
            print("차단바가 열립니다.")
            self.open = True
        else:
            print("차단바를 열 수 없습니다.")

    def close(self, is_pssd):
        if (w_sensor.is_passed = True): 센서에서 차량이 지나갔다고 판단되면
            self.is_pssd = True
        if (self.is_pssd == True):
            print("차단바가 닫힙니다.")
            self.open = False
        else:
            print("빨리 지나가세요.")

    def getOpen(self):
        return self.open, self.is_rgstrd, self.car_num, self.is_pssd

    def setOpen(self, open):
        self.open = open
        self.is_rgstrd = is_rgstrd
        self.car_num = car_num
        self.is_pssd = is_pssd
