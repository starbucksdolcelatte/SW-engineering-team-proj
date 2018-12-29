import random
class Usonic:
    # ultra-sonic sensor

    def get_dist(fr, to):
        # 초음파 센서로 측정한 거리를 리턴하는 함수
        # 테스트를 위해 특정 범위 안에서만 거리를 리턴한다.
        distance = random.randrange(fr,to)
        return distance
