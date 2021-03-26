import requests, json


def start_api(base_url, x_auth_Token):
    headers = {'X-Auth-Token': x_auth_Token, 'Content-Type': 'application/json', }
    data = '{ "problem": 1 }'
    url = base_url + 'start'
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        auth_key = response.json()['auth_key']
    else:
        auth_key = "failed to get key"
    return auth_key


# 현재 시각에 각 자전거 대여소가 보유한 자전거 수 반환 [{'id': 0, 'located_bikes_count' : 4},{}...]
def location_api(base_url, auth_key):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url = base_url + 'locations'
    response = requests.get(url, headers=headers)
    current_locations = response.json()['locations']
    return current_locations


def truck_api(base_url, auth_key):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url = base_url + 'trucks'
    response = requests.get(url, headers=headers)
    current_truck_status: list = response.json()['trucks']
    return current_truck_status


def score_api(base_url, auth_key):
    headers = {'Authorization': auth_key, 'Content-Type': 'application/json', }
    url = base_url + 'score'
    score = requests.get(url, headers=headers).json()
    return score["score"]
