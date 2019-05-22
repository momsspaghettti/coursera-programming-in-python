import requests
import sys

url = sys.argv[1]

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.Timeout:
    print("Timed Out!")
except requests.HTTPError as err:
    code = err.response.status_code
    print("error url: {}, code: {}".format(url, code))
except requests.RequestException:
    print("downloading error: ", url)
else:
    print(response.content)