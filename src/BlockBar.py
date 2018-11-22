    '''
    open: bool

    ---------------------------------
    open(is_rgstrd : bool):None
    is_registered(car_num:str) : bool
    close(is_pssd:bool):None
    get+위 모든 data fields
    set+위 모든 data fields

    '''
# 차단바 제어 프로세스(BlockBar.py)

from car import Car # 파일 이름 car.py, 클래스 이름 Car
from W_Sensor import w_sensor # 파일 이름 W_Sensor, 클래스 이름 w_sensor


class BlockBar:


    def __init__(self):
        self.open = False  #초기 상태 closed

    def is_registered(self, car_num, is_rgstrd):
        if (self.car_num == 등록된 회원이면):
            print("등록된 회원입니다.")
            self.is_rgstrd = True
        else:
            print("등록된 회원이 아닙니다.")

    def open(self, is_rgstrd):
        if (self.is_rgstrd == True):
            print("차단바가 열립니다.")
            self.open = True
        else:
            print("차단바를 열 수 없습니다.")

    def close(self, is_pssd):
        if (self.is_pssd == 차량이 완전히 지나갔다면):
            print("차단바가 닫힙니다.")
            self.open = False

    def getOpen:

    def setOpen:
