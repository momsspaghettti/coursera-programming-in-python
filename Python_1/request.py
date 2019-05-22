import re
import requests


def main(url, substring):

    def searcher(text, string):
        temp_list = re.findall(string, text)
        return len(temp_list)

    def get_code(url):
        if not url.startswith('http'):
            url = "https://" + url

        try:
            return "" or requests.get(url).text
        except (requests.HTTPError, requests.RequestException):
            raise

    try:
        source_code = get_code(url)

        substring_count = searcher(source_code, substring)

        print("'{}' found {} times in '{}'".format(substring, substring_count, url))
    except (requests.HTTPError, requests.RequestException):
        print("Request sending error: invalid URL")


if __name__ == '__main__':
    main("yandex.ru", "div")