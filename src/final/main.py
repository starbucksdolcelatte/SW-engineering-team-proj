from BlockBar import BlockBar
from Kiosk import Kiosk
from ParkingLot import ParkingLot
from ParkingSpot import ParkingSpot
from Camera import Camera
from Pms_db import DBinit
from Stats import Stats
from Car import Car
import time
import random
from datetime import datetime

if __name__ == '__main__':
    random.seed(datetime.now())
    db_path = 'pms_db_fin_2.sqlite'
    in_cam = Camera(db_path, 'entrance')
    out_cam = Camera(db_path, 'exit')
    bar_in = BlockBar(db_path)
    bar_out = BlockBar(db_path)
    mypmsdb = DBinit(db_path)

    #mypmsdb.cur.execute("UPDATE PARKINGLOT_LIST SET Parking_status = 0, Customer_car_num = ''")
    #mypmsdb.conn.commit()
    #mypmsdb.print_table('PARKINGLOT_LIST')

    print("실행할 프로세스를 선택하세요.")
    print("1. 입차   2. 주차   3. 출차   4. 키오스크   5. [관리자]통계")
    a = input()
    print(a," 번을 선택하셨습니다.")


    # 입차
    if(a == '1'):
        # for test : 등록되지 않은 회원
        car_num = in_cam.recog_carnum(0,0)

        # 번호판 인식 : 등록된 회원
        #car_num = in_cam.recog_carnum(1, 0)

        print('인식한 차량 번호는 ', car_num, ' 입니다.')

        # Car 객체 생성
        mycar1 = Car(car_num,db_path)

        # 등록된 회원이면 결제여부 확인,
        # 결제가 모두 완료되어 있으면 차단바 열고 아니면 닫기
        bar_in.blockbar_open(mycar1.car_num)

        if (bar_in.open == True):
            # 3초 동안 차단바 통과
            for i in range(3):
                bar_in.blockbar_close(False)
                time.sleep(1)
            # 차단바 통과 완료
            bar_in.blockbar_close(True)


    # 주차
    elif(a == '2'):
        # ParkingLot 객체 생성
        # ParkingLot 객체는
        # ParkingSpot 객체 리스트를 가지고 있음
        my_pklt = ParkingLot(db_path)

        print("실행할 프로세스를 선택하세요.")
        print("1. 주차하기     2. 차빼기")
        choice = input()

        mypmsdb.cur.execute("SELECT Parking_status FROM PARKINGLOT_LIST")
        spot_list = []
        for row in mypmsdb.cur:
            spot_list.append(row[0])

        pklt_empty = [] # 빈 칸 인덱스 리스트
        pklt_occu = [] # 주차된 칸 인덱스 리스트

        for i in range(len(spot_list)):
            if(spot_list[i] == 0):
                pklt_empty.append(i)
            else:
                pklt_occu.append(i)


        if(choice == '1'):
            my_pklt.display()

            # 주차할 곳
            index_temp = random.randrange(0, len(pklt_empty))
            index = pklt_empty[index_temp]

            if(len(pklt_empty) == 0 ):
                print('주차장에 빈 자리가 없습니다.')
                exit(1)

            # 주차 전 led 상태
            my_pklt.pksp_list[index].get_led()

            # 번호판 인식
            car_num = my_pklt.pksp_list[index].cam.recog_carnum(1,0)
            print('인식한 차량 번호는 ', car_num,' 입니다.')
            my_pklt.pksp_list[index].set_car_num(car_num)

            # Car 객체 생성
            myCar = Car(car_num,db_path)

            # 주차 후
            my_pklt.pksp_list[index].proc_status(1)
            my_pklt.pksp_list[index].set_car_num(car_num)
            my_pklt.pksp_list[index].update_pklt()
            myCar.park(my_pklt.pksp_list[index].get_spot())
            my_pklt.pksp_list[index].set_led()


        elif(choice == '2'):
            # 출차할 곳
            index_temp = random.randrange(0, len(pklt_occu))
            index = pklt_occu[index_temp]

            # 출차 전 led 상태
            my_pklt.pksp_list[index].get_led()

            # Car 객체 생성
            car_num = my_pklt.pksp_list[index].cam.recog_carnum(1,1)
            print('인식한 차량 번호는 ', car_num,' 입니다.')
            myCar = Car(car_num, db_path)

            # 출차 중 주차칸
            my_pklt.pksp_list[index].set_car_num(car_num)
            my_pklt.pksp_list[index].proc_status(2)
            my_pklt.pksp_list[index].set_led()

            # 출차 후 주차칸
            my_pklt.pksp_list[index].proc_status(0)
            my_pklt.pksp_list[index].update_pklt()
            my_pklt.pksp_list[index].set_led()

            # 출차 후 차량
            myCar.move()




    # 출차
    elif(a == '3'):
        now = time.localtime()
        now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        mypmsdb.cur.execute("""SELECT * FROM PARK_PAY WHERE Park_is_paid = 0 AND
         Park_out like ?""", (now_time[:10] + '%',))

        # 출차하는 차량 리스트
        exit_list = []
        for row in mypmsdb.cur:
            print(row)
            if(row is not None):
                exit_list.append(list(row)[1])

        if (len(exit_list) == 0):
            print('출차할 차량이 없습니다.')
            exit(1)

        # 번호판 인식
        index = random.randrange(0, len(exit_list))
        car_num = exit_list[index]

        # Car 객체 생성
        mycar2 = Car(car_num, db_path)
        print('인식한 차량 번호는 ', car_num,' 입니다.')

        # 결제
        mycar2.park_pay(car_num, 0)

        # 등록된 회원이면 결제여부 확인,
        # 결제가 모두 완료되어 있으면 차단바 열고 아니면 닫기
        bar_in.blockbar_open(mycar2.car_num)

        # 3초 동안 차단바 통과
        for i in range(3):
            bar_in.blockbar_close(False)
            time.sleep(1)
        # 차단바 통과 완료
        bar_in.blockbar_close(True)



    # 키오스크
    elif(a == '4'):
        # for test
        # mypmsdb.print_table('PARKINGLOT_LIST')
        myKiosk = Kiosk(db_path)
        print("실행할 프로세스를 선택하세요.")
        print("1. 내 차 찾기     2. 안내원 번호 보기")
        choice = input()
        if(choice == '1'):
            print("차량 번호를 입력하세요.")
            carnum = input()
            myKiosk.get_location(carnum)
        elif(choice == '2'):
            myKiosk.get_staff_tel()

    # 통계
    elif(a == '5'):
        myStats = Stats(db_path)


    # 통계
    elif(a == '5'):
        print("통계 기준을 선택하세요.")
        print("0 : 월별     1 : 요일별     2 : 시간대별")
        criteria = input()
        myStats = Stats(db_path)
        myStats.get_stats(int(criteria))
