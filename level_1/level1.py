#!/usr/bin/python3
import requests
"""level1 module"""

url = "http://158.69.76.135/level1.php"

failed = 0
success = 0
total = 4078

session = requests.Session()

for i in range(total):
    res = session.get(url)
    dict = session.cookies.get_dict()

    data = {'id' : 2529,
            'key': dict['HoldTheDoor'],
            'holdthedoor': 'Envoyer'}
    post = session.post(url, data)
    print("Request #{:d}. Key: {:s}.".format(i, dict['HoldTheDoor']), end=' ')
    if post:
        print("Request OK!")
        success += 1
    else:
        print("Request failed.")
        failed += 1
    session.cookies.clear()

print("Script finished!")
print("{:d} requests sent".format(total + 1))
print("{:d} requests succeded".format(success))
print("{:d} requests failed".format(failed))



# post = session.post(url, data)