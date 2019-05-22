import requests
from json import loads


def get_user_id(uid):

    user_dict = loads(requests.get("https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&"
                                   "access_token=17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711&"
                                   "v=5.71".format(uid)).text)

    return user_dict['response'][0]['id']


def get_friends_list(user_id):

    friends_dict = loads(requests.get("https://api.vk.com/method/friends.get?user_id={0}&fields=bdate&"
                     "access_token=17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711&"
                     "v=5.71".format(user_id)).text)

    friends_list = friends_dict['response']['items']
    return friends_list


def get_bdate(friend):

    if 'bdate' in friend.keys():
        bdate = friend['bdate'].split('.')
        if len(bdate) == 3:
            return int(bdate.pop())

    return None


def get_friends_age_list(friends_list):

    friends_age_list = list()

    for friend in friends_list:
        if not (get_bdate(friend) is None):
            friends_age_list.append(get_bdate(friend))

    return friends_age_list


def get_tuple_list(age_list):

    age_dict = dict()
    age_tuple_list = list()

    for age in age_list:
        if age in age_dict.keys():
            age_dict[age] += 1
        else:
            age_dict.update({age: 1})

    for key in age_dict.keys():
        age_tuple_list.append((2018 - key, age_dict[key]))

    age_tuple_list.sort(key=lambda x: (x[1], -x[0]), reverse=True)

    return age_tuple_list


def calc_age(uid):

    user_id = get_user_id(uid)
    friends_list = get_friends_list(user_id)
    friends_age_list = get_friends_age_list(friends_list)

    return get_tuple_list(friends_age_list)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)