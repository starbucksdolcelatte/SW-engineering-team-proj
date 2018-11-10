 class User:
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
      def __init__(self, car_num):

          self._car_num = car_num

      def get_car_num(self):
          return self._car_num
