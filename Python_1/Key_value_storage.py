import os
import tempfile
import argparse
from json import dumps, loads


storage_path = os.path.join(tempfile.gettempdir(), "storage.data")


def clear():
    with open(storage_path, "w") as f:
        f.write("")


def get_data():
    if not os.path.exists(storage_path):
        return dict()

    with open(storage_path, "r") as f:
        string = f.read()

    if string:
        return loads(string)
    return dict()


def write(key, val):
    temp = dict()
    temp = get_data()
    if key in temp:
        temp[key].append(val)
    else:
        temp[key] = [val]
    with open(storage_path, "w") as f:
        f.write(dumps(temp))
    return {}


def read(key):
    temp = get_data()
    if not key in temp:
        print("No such key!")
    else:
        print(dumps(temp[key]).strip("[]"))
    return {}


parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str)
parser.add_argument("--val", type=str)
parser.add_argument("--clr", action="store_true")
args = parser.parse_args()

if args.clr:
    clear()

if args.key and args.val:
    write(args.key, args.val)
elif args.key:
    read(args.key)
else:
    print("No such argument!")




