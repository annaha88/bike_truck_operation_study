# test1 의 아래 문제점을 보완할 것임
# 1. lack_loc 가 존재하더라도, 트럭 행동중이면 안되는 문제 : lack_loc가 모두 해결될때까지 트럭행동반복하기.

import truck_action
import apis

x_auth_Token = 'd6389067b88ce42fcbcd302472882c21'
current_auth_key = ''
base_url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/'

# # auth key 발급.
if current_auth_key != '':
    auth_key = current_auth_key
else:
    auth_key = apis.start_api(base_url, x_auth_Token)

print("auth_key : ", auth_key)

# 1. 초기의 트럭을 분산시키는 명령 : 한 라인에 한 트럭씩 배정하기.
data = {
    "commands": [{"truck_id": 0, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                 {"truck_id": 1, "command": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                 {"truck_id": 2, "command": [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]},
                 {"truck_id": 3, "command": [0, 0, 1, 1, 1, 0, 0, 0, 0, 0]},
                 {"truck_id": 4, "command": [0, 0, 0, 0, 1, 1, 1, 1, 0, 0]}]
}

# 트럭 분산 : 1분 경과.
truck_action.onetime_simulate_api(base_url, auth_key, data)

# 약 20분간은 자전거가 부족하지 않을 거라는 추정으로 트럭 무행동 돌리기., 여기까지 20분 경과.
data = truck_action.data_no_action()
for i in range(19):
    truck_action.onetime_simulate_api(base_url, auth_key, data)

# 나머지 700분 동안, 9분은 쉬고, 1분은 트럭 행동하는 10분 루틴을 만들것임. 즉 10분씩 70번 반복.(여기서 부족위치가 없으면 무행동 후 다음 루틴으로 넘어감.)
for rep in range(70):
    # 2. 자전거 개수가 1개 이하인 곳 위치 찾기. 찾아서 lack_loc 리스트에 해당 위치 담기.
    lack_loc = []
    loc_status = apis.location_api(base_url, auth_key)

    for i in range(25):
        if loc_status[i]['located_bikes_count'] <= 1:
            lack_loc.append(i)

    # 3-1. 부족한 위치가 없으면(즉 lack_loc 리스트가 비어있으면) 다시 트럭 무행동 10분.
    if not lack_loc:
        data = truck_action.data_no_action()
        for i in range(10):
            truck_action.onetime_simulate_api(base_url, auth_key, data)
    # 3-2. 부족한 위치가 있으면 트럭 부족한 위치 없을때까지 행동, 남은 10분 중 남은 시간 무행동- 해당라인의 할당 트럭이 이동하면서 자전거 1대 수송.
    if lack_loc:
        cnt_min = 0
        while lack_loc:
            data = truck_action.data_no_action()
            truck_status = [0, 0, 0, 0, 0]  # 트럭이 데이터를 받으면 1로 바뀌게 할것임. 이미 작업 할당된 트럭은 쓸수 없다.
            # data 커맨드 생성하기.
            for j in lack_loc:
                truck_id = j % 5
                if truck_status[truck_id] == 0:
                    # 해당 라인의 Max 자전거 위치 찾기.
                    temp = 0
                    loc_status = apis.location_api(base_url, auth_key)
                    for i in range(truck_id, 25, 5):
                        if temp < loc_status[i]['located_bikes_count']:
                            temp = loc_status[i]['located_bikes_count']
                            max_id = i
                    # 이제 트럭행동 커맨드 지정 : 우선 max_id 로 이동해서 자전거 싣고, 부족한곳으로 가서 내려놓고 돌아오기.
                    if max_id > j:
                        data["commands"][truck_id]["command"] = [2] * (max_id // 5) + [5] + [4] * (
                                    (max_id - j) // 5) + [6] + [
                                                                    4] * (j // 5)
                    elif max_id < j:
                        data["commands"][truck_id]["command"] = [2] * (max_id // 5) + [5] + [2] * (
                                    (max_id - j) // 5) + [6] + [
                                                                    4] * (j // 5)
                    else:  # max_id와 j(부족위치)가 동일하면 아무행동 안함.
                        pass

                    truck_status[truck_id] = 1  # 해당 아이디 트럭 작업 할당 받음.
                    lack_loc.remove(j)  # 부족위치 지우기.
            # 이제 명령 실행.
            # 행동 명령 1분
            truck_action.onetime_simulate_api(base_url, auth_key, data)
            cnt_min += 1

        # 남은 시간 무행동(10분 - cnt_min)
        data = truck_action.data_no_action()
        for i in range(10 - cnt_min):
            truck_action.onetime_simulate_api(base_url, auth_key, data)

# 점수 얻기
score = apis.score_api(base_url, auth_key)
print(score)
