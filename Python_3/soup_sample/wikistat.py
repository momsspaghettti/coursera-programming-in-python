from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}

    for file in files.keys():
        files[file] = []
        with open("{}{}".format(path, file), encoding="UTF-8") as reader:
            refs_list = link_re.findall(reader.read())

        for ref in refs_list:
            if (ref in files.keys()) and (ref != file) and (ref not in files[file]):
                files[file].append(ref)

    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)

    level = dict.fromkeys(files, -1)
    level[start] = 0
    stack = [start]

    while stack:
        v = stack.pop(0)
        for w in files[v]:
            if level[w] == -1:
                stack.append(w)
                level[w] = level[v] + 1

    bridge = [end]
    pos = level[end]

    while pos != 0:
        for lv in level.keys():
            if (level[lv] == pos - 1) and (bridge[len(bridge) - 1] in files[lv]):
                bridge.append(lv)
                pos -= 1
                break
    # TODO Добавить нужные страницы в bridge
    return bridge


def get_imgs_count(body):
    count = 0

    tags = body('img')

    for tag in tags:
        if 'width' in tag.attrs:
            if int(tag['width']) >= 200:
                count += 1

    return count


def get_headers_count(body):
    count = 0

    tags = {}
    for i in range(1, 7):
        tags['h{}'.format(i)] = body('h{}'.format(i))

    for head in tags.keys():
        for tag in tags[head]:
            for child in list(tag.children):
                if str(child.string)[0] in ['E', 'T', 'C']:
                    count += 1

    return count


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


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file), encoding="UTF-8") as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        imgs = get_imgs_count(body)  # Количество картинок (img) с шириной (width) не меньше 200
        headers = get_headers_count(body)  # Количество заголовков, первая буква текста внутри которого: E, T или C
        linkslen = get_links_len(body)  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = get_lists_count(body)  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out
