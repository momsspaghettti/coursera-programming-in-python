import requests


if __name__ == '__main__':
    resp = requests.put('http://79.137.175.13/submissions/super/duper/secret/', headers={'Authorization': 'Basic Z2FsY2hvbm9rOmt0b3RhbWE='})
    print(resp.text.encode('utf-8').decode('unicode-escape'))