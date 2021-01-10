#!/usr/bin/python3
import requests
"""level0 module"""

url = "http://158.69.76.135/level0.php"
# res = requests.get(url)
# print(res)

data = {'id' : 2529,
        'holdthedoor': 'Envoyer'}

for i in range(1024):
    post = requests.post(url, data)
    print("Request #{:d}. Status code {:d}".format(i, post.status_code))
