import requests, json
import time

import current_status, apis


def data_no_action():
    data = {
        "commands": [{"truck_id": 0, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                     {"truck_id": 1, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                     {"truck_id": 2, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                     {"truck_id": 3, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                     {"truck_id": 4, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]
    }
    return data


def simulate_api(url, auth_key, data):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url = url + 'simulate'
    for i in range(120):
        truck_put_res = requests.put(url, headers=headers, data=json.dumps(data))
        if i % 10 == 0:
            time.sleep(0.1)
    simulated_r = truck_put_res.json()
    return simulated_r['status']


# 위에까지는 그냥 Nothing 접근. 아무 행동도 하지 않고 서버 돌리기.

# 여기부터 알고리즘 짜기. 접근은. 일단 자전거 개수가 1 이하인 자전거 대여소를 구하고, 거기서 가까운 위치에 있는 트럭 이용해서 자전거 1대 가져다 놓기.
# 즉 자전거 부족한 곳을 채워넣기만 하는 1차적인 접근
# min 자전거 개수 얻은 후에 그 수가 1 이하이면, 해당 위치 근처 트럭 찾은 후, 자전거 3 이상인 위치에서 1개를 가져다가 자전거 하차 하도록 만들기.

# 이거는 720번 돌린후 기준으로, min 값에 따라서 data 를 입력해본 것임.(즉 아주 대충)
def algo_data_for_action():
    data = {
        "commands": [{"truck_id": 0, "command": [5, 2, 2, 2, 2, 6, 4, 4, 4, 4]},
                     {"truck_id": 1, "command": [5, 2, 2, 1, 1, 1, 6, 3, 3, 4]},
                     {"truck_id": 2, "command": [2, 5, 2, 6, 4, 4, 0, 0, 0, 0]},
                     {"truck_id": 3, "command": [1, 5, 2, 6, 3, 0, 0, 0, 0, 0]},
                     {"truck_id": 4, "command": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]
    }
    return data


def algo_simulate_api(url, auth_key):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url_simula = url + 'simulate'
    truck_put_res = requests.put(url_simula, headers=headers, data=json.dumps(data2))

    simulated_r = truck_put_res.json()
    return simulated_r['status']


def onetime_simulate_api(url, auth_key, data):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url = url + 'simulate'
    truck_put_res = requests.put(url, headers=headers, data=json.dumps(data))
    simulated_r = truck_put_res.json()
    return simulated_r['status']
