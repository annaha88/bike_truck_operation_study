import apis


def max_count_location(location_lst):
    max_count = 0
    for i in range(len(location_lst)):
        if location_lst[i]['located_bikes_count'] > max_count:
            max_count = location_lst[i]['located_bikes_count']
            max_id = i
    return max_id, max_count


def min_count_location(location_lst):
    min_lst = []
    min_count = 1000
    for i in range(len(location_lst)):
        if location_lst[i]['located_bikes_count'] <= min_count:
            min_count = location_lst[i]['located_bikes_count']
            min_id = i
            min_lst.append({"location_id": min_id, "min_count": min_count})
    return min_lst
