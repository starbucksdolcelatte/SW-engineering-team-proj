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
def DB_insert(attr, table):
    # 구현
    # attr의 형태는 ',' 또는 ' '등으로 각 튜플 값을 구분한 attribute 값 string
    # table의 형태는 table 이름
    # table에 신규 attribute 삽입
    return 0




######################################################
# Django DB 값 수정
# input :
# return : 0
def DB_update_set ():
    # table의 특정 attribute 값 수정
    return 0




######################################################
# Django DB 값 삭제
# input :
# return : 0
def DB_delete ():
    # table의 특정 attribute 값 삭제

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
    1) is_allowed 값이 true면
    1-1) status = true

    2) is_allowed 값이 false면
    2-1) status = false

    3) return None
    '''



######################################################
# 층마다 남은 자리수 계산 ( 전광판 )
# input : string floor (몇층인지 : DB의 층 표현 포맷을 따름)
# return : int num_empty
# get floor info
def get_flr_info(floor):
    # 실시간 주차장 테이블에서
    # unit_id == floor && status == empty 인
    # attribute의 총 개수 받아와서
    # num_empty에 저장 후 return
    return num_empty



######################################################
# 칸마다 occupied rate 분석 후 주차 칸 occupied rate DB에 update
# input : image (주차장), string (구역(알파벳))
# return : None
# set unit occupied rate
def set_occu_rate(img, zone):
    # 이 함수는 각 zone마다 설치된 라즈베리파이에서 개별적으로 돌아갈 것
    # 각 라즈베리파이마다 고유값이 있고 그 고유값에 따라 zone이 결정됨
    # 이미지를 분석해서 해당 zone의 1...n번째 칸(unit)의 occupied rate 구함
    # 실시간 주차장 occupied 수치 테이블에서 zone이 일치하는 attr에 대하여
    # occu_rate를 update
    # DB_update_set() 함수 씀
    return None



######################################################
# 칸마다 주차 상태 분석 후 주차 칸 상태 DB에 update
# 주차 상태는 occupied, empty, leaving(출차중)
# input : string zone(구역(알파벳))
# return : None
# set unit status
def set_unit_status(zone):
    # 이 함수는 각 zone마다 설치된 라즈베리파이에서 개별적으로 돌아갈 것
    # 각 라즈베리파이마다 고유값이 있고 그 고유값에 따라 zone이 결정됨
    # 실시간 주차장 occupied 수치 테이블에서 zone이 일치하는 attr에 대하여
    # occu_rate 1초에 한번씩 가져와서 list에 넣음.
    # occu_rate 1초 전과 지금의 변화량을 가져와서 또다른 list에 넣음.
    # 1초마다 갱신(옛날꺼 하나 지우고 지금꺼 하나 추가),
    # 지난 n초 간의 occu_rate 변화량이 음수이고 변화량 평균이 criteria 이상이면
    # 출차중으로 판단한다.

    # 변화량 평균이 criteria 이하인 것들 중에
    # occu_rate 평균이 기준치 이상이면 occupied
    # occu_rate 평균이 기준치 이하이면 num_empty

    # 결과를 DB에 update
    # DB_update_set() 함수 씀
    return None
