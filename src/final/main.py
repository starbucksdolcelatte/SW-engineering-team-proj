from BlockBar import BlockBar
from Kiosk import Kiosk
from ParkingLot import ParkingLot
from ParkingSpot import ParkingSpot
from Camera import Camera
from User import User
from Pms_db import DBinit
from Stats import Stats

if __name__ == '__main__':

    db_path = 'pms_db_fin_1.sqlite'
    in_cam = Camera(db_path, 'entrance')
    out_cam = Camera(db_path, 'exit')
    block_bar_in = BlockBar(db_path)
    block_bar_out = BlockBar(db_path)



    print("실행할 프로세스를 선택하세요.")
    print("1. 입차   2. 출차   3. 주차   4. 키오스크   5. 통계")
    a = input()
    print(a,"번을 선택하셨습니다.")

    # 입차
    if(a == 1):
        # 번호판 인식
        car_num = in_cam.recog_carnum(1)[0]
        print('인식한 차량 번호는 ',car_num,' 입니다.')
        # Car 객체 생성
        mycar1 = Car(car_num,db_path)
        # 등록된 회원이면 결제여부 확인,
        # 결제가 모두 완료되어 있으면 차단바 열고 아니면 닫기
        block_bar_in.blockbar_open(mycar1.car_num)

    # 출차
    elif(a == 2):
        # 번호판 인식
        car_num = pklt_cam.recog_carnum(1)[0]
        # Car 객체 생성
        mycar2 = Car(car_num, db_path)
        print('인식한 차량 번호는 ',car_num,' 입니다.')
        # 결제
        mycar2.park_pay()
        # 무료 주차 시간, 주차요금 구해 저장하기
        mycar2.set_pay_amount()
        # Car의 data fields 값을 PARK_PAY 테이블에 삽입하기
        mycar2.insert_ppay()
        # PARKINGLOT_LIST 튜플 업데이트하기
        # my_pklt.pksp_list[0][0][0].update_pklt()


    # 주차
    elif(a == 3):
        # ParkingLot 객체 생성
        # ParkingLot 객체는
        # ParkingSpot 객체 리스트를 가지고 있음
        my_pklt = ParkingLot(db_path)

        print("실행할 프로세스를 선택하세요.")
        print("1. 주차하기     2. 차빼기")
        choice = input()

        if(choice == 1):
            # 주차 전 B1-A1 구역
            my_pklt.pksp_list[0][0][0].set_led()
            # 번호판 인식
            car_num = pklt_cam.recog()[0]
            print('인식한 차량 번호는 ',car_num,' 입니다.')
            # Car 객체 생성
            myCar = Car(car_num,db_path)
            # 주차 후  B1-A1 구역
            my_pklt.pksp_list[0][0][0].get_status(1)
            my_pklt.pksp_list[0][0][0].set_car_num(car_num)
            my_pklt.pksp_list[0][0][0].update_pklt()
            myCar.park('B1-A1')
            # 주차 후
            my_pklt.pksp_list[0][0][0].set_led()

        elif(choice == 2):
            # 출차 중  B1-A1 구역
            my_pklt.pksp_list[0][0][0].get_status(0)
            # 출차 후  B1-A1 구역
            my_pklt.pksp_list[0][0][0].set_led()
            myCar.move()

    # 키오스크
    elif(a == 4):
        myKiosk = Kiosk(db_path)
        print("실행할 프로세스를 선택하세요.")
        print("1. 내 차 찾기     2. 안내원 번호 보기")
        choice = input()
        if(choice == 1):
            print("차량 번호를 입력하세요.")
            carnum = input()
            myKiosk.get_location(carnum)
        elif(choice == 2):
            myKiosk.staff_tel()

    # 통계
    elif(a == 5):
        print("통계 기준을 선택하세요.")
        print("0 : 월별     1 : 요일별     2 : 시간대별")
        criteria = input()
        myStats = Stats(db_path)
        myStats.get_stats(criteria)
