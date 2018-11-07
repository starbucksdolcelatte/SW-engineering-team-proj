# 전역변수로 상수 선언
MON = 0
DAY = 1
HOUR = 2





######################################################
# 번호판 인식
# input : image (image of vehicle registration plate)
# return : string car_num "15머1414" (string of)
def get_car_num():
    #구현부
    # 출력 포맷)"15머1414"
    return string


######################################################
# Django DB에 새로운 attr 삽입
# input : string attr, string table
# return : 0
def insert(attr, table):
    # 구현
    # attr의 형태는 ',' 또는 ' '등으로 각 튜플 값을 구분한 attribute 값 string
    # table의 형태는 table 이름
    # table에 신규 attribute 삽입
    return 0




######################################################
# Django DB 값 수정
# input : string attr, string table
# return : 0
def (src, table):
    # src의 형태는 ',' 또는 ' '등으로 각 튜플 값을 구분한 attribute 값 string
    # table의 형태는 table 이름
    # table에 신규 attribute 저장
    return 0




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





######################################################
# 차단바 올리기
# input : boolean is_allowed
# return : int angle
def open_block_bar(is_allowed):
    #구현부
    '''
    변수 1 angle = 0

    1) is_allowed 값이 true면
    1-1) angle = 90

    2) is_allowed 값이 false면
    2-1) 아무 동작 안함.

    3) return angle
    '''



######################################################
#
