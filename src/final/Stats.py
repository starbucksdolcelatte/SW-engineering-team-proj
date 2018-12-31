import datetime
import calendar
import locale
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from Pms_db import DBinit

class Stats:
    '''
    sdate : string
    edate : string
    criteria : integer
    admin_id : string
    admin_pw : string
    -------------------
    get_stats(self, criteria) # 기준에 따른 통계 결과를 그래프로 리턴
    mon_stats(self, sdate, edate) # 월별 통계 결과를 리스트로 리턴
    day_stats(self, sdate, edate) # 요일별 통계 결과를 리스트로 리턴
    hour_stats(self, sdate, edate) # 시간대별 통계 결과를 리스트로 리턴
    '''

    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgunsl.ttf").get_name()
    rc('font', family=font_name)
    locale.setlocale(locale.LC_ALL, '')
    stat_list = []

    def __init__(self, db_path):
        # db_path에 대하여 SQLite DB 연결
        self.mypmsdb = DBinit(db_path)
        # 월 0 요일 1 시간 2
        self._criteria = 0
        self._sdate = datetime.datetime.now().strftime("%Y-%m-%d")
        self._edate = datetime.datetime.now().strftime("%Y-%m-%d")
        self._admin_id = 'hufs14'
        self._admin_pw = 'onframe341'

        print('ID 를 입력하세요.')
        my_id = input()
        if(my_id != self._admin_id):
            print('존재하지 않는 ID입니다.')
            return
        else:
            print('비밀번호를 입력하세요.')
            my_pw = input()
            if(my_pw != self._admin_pw):
                print('비밀번호가 틀렸습니다.')
                return


        print("통계 기준을 선택하세요.")
        print("0 : 월별     1 : 요일별     2 : 시간대별")
        criteria = input()
        self.criteria = int(criteria)

        print('통계 시작날짜를 입력하세요. yyyy-mm-dd')
        s_date = input()
        self.sdate = s_date
        print('통계 종료날짜를 입력하세요. yyyy-mm-dd')
        e_date = input()
        self.edate = e_date

        # 통계 그래프 보여주기
        self.get_stats(int(criteria))



    def get_stats(self, criteria):

        """ 테스트용 """
        print('통계 기준 : ',self.criteria)
        print('통계 시작 날짜 : ', self.sdate)
        print('통계 종료 날짜 : ', self.edate)
        """         """

        # 0 월별 1 요일별 2 시간대별
        if criteria == 0:
            self.stat_list = self.mon_stats(self.sdate, self.edate)
            # print(self.stat_list)
        elif criteria == 1:
            self.stat_list = self.day_stats(self.sdate, self.edate)
            # print(self.stat_list)
        elif criteria == 2:
            self.stat_list = self.hour_stats(self.sdate, self.edate)
        else:
            print("wrong criteria")
            return
        print(self.stat_list)

        # 통계 그래프 그리기
        # 데이터가 없는 달, 요일은 출력되지 않음
        ####### 추가부분 ##############################################
        fig = plt.figure()
        width = 0.2

        # 세개의 그래프
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)

        crit = []
        num_of_cars = []
        total_time = []
        total_fee = []

        # 월별로 되어있는 stat_list를 기준, 차량대수, 총시간, 총요금의 리스트로
        for i in self.stat_list:
            crit.append(i[0])  # 월/요일
            num_of_cars.append(i[1])
            total_time.append(i[2])
            total_fee.append(i[3])

        # 요일별 기준일 경우 0~6으로 표시되는 요일을 locale설정에 맞춰 출력 - 예: 일, 월 // Sun, Mon ..
        if criteria == 1:
            for i in range(len(crit)):
                if crit[i] == 0:
                    crit[i] = calendar.day_abbr[6]
                else:
                    crit[i] = calendar.day_abbr[int(crit[i]) - 1]

        # 막대그래프를 그림
        ax1.bar(crit, num_of_cars, width, color='IndianRed')
        ax2.bar(crit, total_time, width, color='IndianRed')
        ax3.bar(crit, total_fee, width, color='IndianRed')

        if criteria == 0:
            plt.xlabel("MONTHLY REPORT")
        elif criteria == 1:
            plt.xlabel("REPORT BY DAY")
        ax1.set_ylabel('NUMBER OF CARS')
        ax2.set_ylabel('TOTAL TIME(hour)')
        ax3.set_ylabel('TOTAL FEE')

        plt.show()

        #############################################################
        return self.stat_list


    #   월별 통계를 구함
    #   sdate 포함, edate 포함하지 않음
    def mon_stats(self, sdate, edate):
        stat_list = []
        # SQL 쿼리
        self.mypmsdb.cur.execute("select strftime('%m', Park_in) 날짜, count(*) 차량대수, \
                                    (sum(strftime('%s', Park_out) - strftime('%s', Park_in)))/3600 총시간, \
                            sum(Park_pay_amount) 총요금 from PARK_PAY where Park_out between ? and ? group by 날짜",
                            (sdate, edate))
        rows = self.mypmsdb.cur.fetchall()

        for row in rows:
            stat_tup = list(row)
            stat_list.append(stat_tup)

        return stat_list


    #   요일별 통계를 구함
    #   sdate 포함, edate 포함하지 않음
    #   0~6 일~토
    def day_stats(self, sdate, edate):
        stat_list = []
        self.mypmsdb.cur.execute("select strftime('%w', Park_in) 요일, count(*) 차량대수, \
                                    (sum(strftime('%s', Park_out) - strftime('%s', Park_in)))/3600 총시간, \
                            sum(Park_pay_amount) 총요금 from PARK_PAY where Park_out between ? and ? group by 요일",
                            (sdate, edate))
        rows = self.mypmsdb.cur.fetchall()

        for row in rows:
            stat_tup = list(row)
            stat_list.append(stat_tup)

        return stat_list



    def hour_stats(self, sdate, edate):
        pass

    @property
    def sdate(self):
        return self._sdate

    @sdate.setter
    def sdate(self, new_sdate):
        # 통계 시작 기준 날짜가 오늘 날짜보다 이전이어야, 그렇지않으면 무시
        convert_new_sdate = datetime.datetime.strptime(new_sdate, "%Y-%m-%d").date()
        if convert_new_sdate < datetime.datetime.today().date():
            self._sdate = new_sdate

    @property
    def edate(self):
        return self._edate

    @edate.setter
    def edate(self, new_edate):
        # 통계 끝 기준 날짜가 오늘 날짜보다 이전이어야, 그렇지않으면 무시
        convert_new_edate = datetime.datetime.strptime(new_edate, "%Y-%m-%d").date()
        if convert_new_edate < datetime.datetime.today().date():
            self._edate = new_edate

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, new_criteria):
        # 기준 0, 1, 2 제외 무시
        if new_criteria == 0 or new_criteria == 1 :  # 기준 0, 1 제외 무시 // 월별, 요일별 통계만
        # if new_criteria == 0 or new_criteria == 1 or new_criteria == 2:
            self._criteria = new_criteria
