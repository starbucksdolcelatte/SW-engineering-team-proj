'''
id,pw는 웹에서 구현될거라 뺐음.
이 클래스 다이어그램은 파이썬 모듈만 포함이 됨.
sdate:str
edate:str
criteria: int

get_stats(criteria):int list


mon_stats(sdate, edate):int list


day_stats(sdate, edate):int list
hour_stats(sdate, edate):int list
get+위 모든 data fields
set+위 모든 data fields

'''
import datetime
import sqlite3



class Stats:

    con = sqlite3.connect("C:\\setermprj\\test.db")
    cursor = con.cursor()

    stat_list = []

    def __init__(self):
        self._sdate = datetime.datetime.now().strftime("%Y-%m-%d")
        self._edate = datetime.datetime.now().strftime("%Y-%m-%d")

        # 일단 월 0 요일 1 시간 2
        self._criteria = 0

    def get_stats(self, criteria):

        """ 테스트용 """
        print(self.criteria)
        print(self.sdate)
        print(self.edate)
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
        return self.stat_list



    def mon_stats(self, sdate, edate):
        stat_list = []
        # SQL 쿼리 //  통계확인시점 기준으로 pay안한사람은 안나타나게되어있
        self.cursor.execute("select strftime('%Y-%m', InTime) 날짜, count(*) 차량대수, \
        sum(strftime('%s', OutTime) - strftime('%s', InTime)) 총시간,  sum(Amount) 총요금 \
        from park join park_payment on park.Number = park_payment.Number and park.InTime between '" + sdate + "' and '" + edate + "' group by 날짜")
        rows = self.cursor.fetchall()

        for row in rows:
            stat_tup = list(row)
            stat_list.append(stat_tup)

        return stat_list

    def day_stats(self, sdate, edate):
        stat_list = []
        self.cursor.execute("select strftime('%w', InTime) 요일, count(*) 차량대수, \
        sum(strftime('%s', OutTime) - strftime('%s', InTime)) 총시간,  sum(Amount) 총요금 \
        from park join park_payment on park.Number = park_payment.Number and park.InTime between '" + sdate + "' and '" + edate + "' group by 요일")
        rows = self.cursor.fetchall()

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
        # 통계 시작 기준 날짜가 오늘 날짜보다 앞이어야
        convert_new_sdate = datetime.datetime.strptime(new_sdate, "%Y-%m-%d").date()
        if convert_new_sdate < datetime.datetime.today().date():
            self._sdate = new_sdate

    @property
    def edate(self):
        return self._edate

    @edate.setter
    def edate(self, new_edate):
        # 통계 끝 기준 날짜가 오늘 날짜보다 앞이어야
        convert_new_edate = datetime.datetime.strptime(new_edate, "%Y-%m-%d").date()
        if convert_new_edate < datetime.datetime.today().date():
            self._edate = new_edate

    @property
    def criteria(self):
        return self._criteria

    @criteria.setter
    def criteria(self, new_criteria):
        if new_criteria == 0 or new_criteria == 1 or new_criteria == 2:
            self._criteria = new_criteria

a = Stats()

a.criteria = 1
a.sdate = '2018-10-01'
a.edate = '2018-11-04'

a.get_stats(a.criteria)
