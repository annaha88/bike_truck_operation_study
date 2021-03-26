# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
import apis
import current_status
import truck_action

x_auth_Token = '14d4fb8fa266b047f49823c34b0532c6'
current_auth_key = ''
base_url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/'

if __name__ == '__main__':
    # # auth key 발급.
    # auth_key = apis.start_api(base_url, x_auth_Token)
    if current_auth_key != '':
        auth_key = current_auth_key
    else:
        auth_key = apis.start_api(base_url, x_auth_Token)

    print(auth_key)

    # 현재 자전거 대여소 현황 리스트 얻기
    location_lst = apis.location_api(base_url, auth_key)
    #  현재 Max 자전거 개수와 해당 대여소 위치 찾기
    max_loc_cnt = current_status.max_count_location(location_lst)
    min_loc_cnt = current_status.min_count_location(location_lst)
    print(max_loc_cnt, min_loc_cnt)

    # 현재 Truck 위치와 상태
    trucks_lst = apis.truck_api(base_url, auth_key)
    print(trucks_lst[-1])  # id가 4인 트럭 상태

    # 트럭 행동 data 얻기
    data_nothing = truck_action.data_no_action()
    data_something = truck_action.algo_data_for_action()

    # simulation 돌리기

    for i in range(6):
        server_status = truck_action.simulate_api(base_url, auth_key, data_nothing)
        # server_status = truck_action.onetime_simulate_api(base_url, auth_key, data_something)

    print(server_status)

    # 점수 얻기
    score = apis.score_api(base_url, auth_key)
    print(score)
