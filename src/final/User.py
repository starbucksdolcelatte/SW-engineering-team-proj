
          '''
        car_num : str
        card_info : str list
        name : str
        phone : str
        mall_cost : int
        mall_pay_time : str
        park_cost : int
        is_paid_park : bool
        park_pay_time : str
        free_park : int

        ----------------------------------------
        pay(park_cost: int) : is_paid_park : bool
        get+위 모든 data fields
        set+위 모든 data fields

          '''
import sqlite3


class User:

    con = sqlite3.connect("C:\\setermprj\\test.db")
    cursor = con.cursor()

    def __init__(self, car_num):
        self._car_num = car_num
        # 아마 통합과정에서 이쪽이 달라지지않을까 생각중.. user 클래스 안에서 db연결을 할것같진않으니
        self.cursor.execute("select * from customer_list where customer_car_num = ?", (car_num,))
        customer_info = self.cursor.fetchone()

        # customer_list
        # 차번호 | 카드번호 | 차주이름 | 휴대폰번호
        self._name = customer_info[2]
        self._card_info = customer_info[1]
        self._phone = customer_info[3]

        # 결제이후 초기화되는 속성들
        self._mall_cost = None
        self._mall_pay_time = None
        self._park_cost = None
        self._is_paid_park = None
        self._park_pay_time = None
        self._free_park = None

    # 쇼핑 - 액수, 시간 업데이트
    def update_shopping_info(self, purchase_amount, purchase_time):
        self.mall_cost = purchase_amount
        self.mall_pay_time = purchase_time

    # 주차 - 요금, 결제 여부, 시각 업데이트
    def update_park_info(self, park_fee, paid, pay_time):
        self.park_cost = park_fee
        self.is_paid_park = paid
        self.park_pay_time = pay_time

    @property
    def car_num(self):
        return self._car_num

    @car_num.setter
    def car_num(self, new_car_num):
        self._car_num = new_car_num

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def card_info(self):
        return self._card_info

    @card_info.setter
    def card_info(self, new_card_info):
        self._card_info = new_card_info

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_phone):
        self._phone = new_phone

    @property
    def mall_cost(self):
        return self._mall_cost

    @mall_cost.setter
    def mall_cost(self, new_mall_cost):
        self._mall_cost = new_mall_cost

    @property
    def mall_pay_time(self):
        return self._mall_pay_time

    @mall_pay_time.setter
    def mall_pay_time(self, new_mall_pay_time):
        self._mall_pay_time = new_mall_pay_time

    @property
    def park_cost(self):
        return self._park_cost

    @park_cost.setter
    def park_cost(self, new_park_cost):
        self._park_cost = new_park_cost

    @property
    def is_paid_park(self):
        return self._is_paid_park

    @is_paid_park.setter
    def is_paid_park(self, b):
        self._is_paid_park = b

    @property
    def park_pay_time(self):
        return self._park_pay_time

    @park_pay_time.setter
    def park_pay_time(self, new_park_pay_time):
        self._park_pay_time = new_park_pay_time

    @property
    def free_park(self):
        return self._free_park

    @free_park.setter
    def free_park(self, new_free_park):
        self._free_park = new_free_park
