# 전역변수로 상수 선언
MON = 0
DAY = 1
HOUR = 2



######################################################
# 관리자 로그인 기능
# 장고 서버에서 관리자 페이지를 기본으로 제공하므로,
# 장고 서버에서 로그인 기능 구현 가능할 것으로 보입니다.



######################################################
# 기준에 따른 주차장 통계 제공 기능
# library : Bokeh (검색해보세요)
# https://bokeh.pydata.org/en/latest/docs/gallery.html
# 웹 브라우저 상에서의 시각화에 효과적
# Python의 interactive visualization library
# plot을 HTML로 export 하여, 웹 브라우저 상에서 확인할 수 있고,
# interactive하게 조작 가능 : 예 - 선택한 부분만 히스토그램 활성화 가능
# input : const int standard(MON or DAY or HOUR), string start_date, string end_date
# return : None
def get_stats(std, s_date, e_date):
    # 구현부
    # 기간에 따라 DB에서 차량 수, 금액 데이터 긁어와서 show 해서 웹상에 뿌린다.
    # 참고 : https://datascienceschool.net/view-notebook/b03af554a1494f159fc94d65d70fe7b2/

    switch(std):
    case MON:
    case DAY:
    case HOUR:
    default:

    return None
