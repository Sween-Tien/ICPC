#!/usr/bin/python3

import sys
import requests
import random

addr = [
    "http://192.168.12.101:12306", "http://192.168.12.102:12306",
    "http://192.168.12.103:12306", "http://192.168.12.104:12306"
]


if __name__ == "__main__":
    filename = sys.argv[1]
    data = open(filename, "rb")
    requests.post(random.choice(addr), data)


