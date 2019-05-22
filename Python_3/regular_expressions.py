import requests
import re
from bs4 import BeautifulSoup
import os
import lxml


def get_link_count(links_list):
    max_len = 1

    for i in range(len(links_list)):
        if str(links_list[i])[1] == 'a':
            max_len += 1
        else:
            break

    return max_len


def get_links_len(body):
    link_len = 0

    tags = body('a')
    for tag in tags:
        tmp_len = get_link_count(tag.find_next_siblings())
        if tmp_len > link_len:
            link_len = tmp_len

    return link_len


def get_lists_count(body):
    count = 0
    tags = body.find_all(['ul', 'ol'])

    for tag in tags:
        if not tag.find_parents(['ul', 'ol']):
            count += 1

    return count


if __name__ == '__main__':
    path = "C://Users//Иван//Desktop//soup_sample//wiki//"
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    start = 'Stone_Age'

    for file in files.keys():
        files[file] = []
        with open("{}{}".format(path, file), encoding="UTF-8") as reader:
            refs_list = link_re.findall(reader.read())

        for ref in refs_list:
            if (ref in files.keys()) and (ref != file) and (ref not in files[file]):
                files[file].append(ref)

    level = dict.fromkeys(files, -1)
    level[start] = 0
    stack = [start]

    while stack:
        v = stack.pop(0)
        for w in files[v]:
            if level[w] == -1:
                stack.append(w)
                level[w] = level[v] + 1

    bridge = ['Python_(programming_language)']
    pos = level['Python_(programming_language)']

    while pos != 0:
        for lv in level.keys():
            if (level[lv] == pos - 1) and (bridge[len(bridge) - 1] in files[lv]):
                bridge.append(lv)
                pos -= 1
                break

    out = {}
    count = 0
    tmp_count = 0
    for file in bridge:
        p_list = []
        with open("{}{}".format(path, file), encoding="UTF-8") as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")
        # TODO посчитать реальные значения
        imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = get_links_len(body) # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = get_lists_count(body)  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

print(out)