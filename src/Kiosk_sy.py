import sqlite3

class Kiosk:
    def __init__(self, db_filename, staff_tel):
        print("Kiosk 객체가 생성되었습니다.")
        self.__staff_tel = staff_tel
        print("Staff Tel. = " + self.__staff_tel)

        # SQLite DB 연결
        # db_filename 있으면 연결, 없으면 새로 생성
        self.conn = sqlite3.connect(db_filename, detect_types=sqlite3.PARSE_DECLTYPES)
        # Connection 으로부터 Cursor 생성
        self.cur = self.conn.cursor()

    @property
    def staff_tel(self):
        return self.__staff_tel

    # 원래 설계는 뒤 4자리만 누르는 걸로 했지만
    # 그냥 12가1234 이렇게 앞숫자 2자리, 한글 한 자리, 뒤 숫자 4자리의 조합을 모두 입력하는 것으로 한다.
    def where_is_my_car(self, car_num):
        self.cur.execute("SELECT parking_spot FROM PARKINGLOT_LIST WHERE Customer_car_num = ?", (car_num,))
        location = self.cur.fetchone()
        if location is None :
            print('해당 번호의 차량이 없습니다.')
            return None
        else :
            print('고객님의 차량은 ', location[0], ' 에 있습니다.')
            return location[0]
