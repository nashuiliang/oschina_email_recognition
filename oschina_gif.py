#!/usr/bin/env python
# coding=utf-8

import logging
import os
import requests

url = "http://my.oschina.net/action/textImage/new_user_email?id={}"
max_user_id = 10000
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2327.5 Safari/537.36"
}

base_path = os.path.join(os.path.dirname(__file__), "oschina_all_gif")

for i in xrange(1, max_user_id):
    response = requests.get(url.format(i), headers=headers, stream=True)
    if response.status_code == 200 and response.text:
        logging.warn(("GIF******", i))
        with open(os.path.join(base_path, "{}.gif".format(i)), "wb") as f:
            for chunk in response.iter_content():
                f.write(chunk)
