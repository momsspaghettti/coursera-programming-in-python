def calculate(data, findall):
    matches = findall(r'[abc][+-]?[=][abc][+-][0-9]{1,}|[abc][+-]?[=][+-]?[0-9]{1,}|[abc][+-]?[=][abc]')

    for match in matches:
        if get_func_numb(match) == 1:
            func_one(match, data)
        if get_func_numb(match) == 2:
            func_two(match, data)
        if get_func_numb(match) == 3:
            func_three(match, data)

    return data


def get_func_numb(match):
    arr = match.split('=')

    if (('a' in arr[1]) or ('b' in arr[1]) or ('c' in arr[1])) and (len(arr[1]) != 1):
        return 1

    if (('a' in arr[1]) or ('b' in arr[1]) or ('c' in arr[1])) and (len(arr[1]) == 1):
        return 3

    return 2


def func_one(match, data):
    arr = match.split('=')

    if len(arr[0]) == 1:
        data[arr[0][0]] = data[arr[1][0]] + int((arr[1])[1:])
    else:
        if arr[0][1] == '+':
            data[arr[0][0]] += data[arr[1][0]] + int((arr[1])[1:])
        else:
            data[arr[0][0]] -= data[arr[1][0]] + int((arr[1])[1:])


def func_two(match, data):
    arr = match.split('=')

    if len(arr[0]) == 1:
        data[arr[0][0]] = int(arr[1])
    else:
        if arr[0][1] == '+':
            data[arr[0][0]] += int(arr[1])
        else:
            data[arr[0][0]] -= int(arr[1])


def func_three(match, data):
    arr = match.split('=')

    if len(arr[0]) == 1:
        data[arr[0][0]] = data[arr[1][0]]
    else:
        if arr[0][1] == '+':
            data[arr[0][0]] += data[arr[1][0]]
        else:
            data[arr[0][0]] -= data[arr[1][0]]