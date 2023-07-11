# -*- coding: utf-8 -*-
# @Time    : 11/7/2023 下午 1:37
# @Author  : dynasty919
# @Email   : dynasty919@163.com
# @File    : main.py
# @Software: PyCharm

import re
import urllib.request
import os
import time
import random

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

def main():
    galleries = []
    while 1:
        url = input("please input a gallery url(press Enter to finish):")
        if url == "":
            break
        else:
            galleries.append(url)

    if len(galleries) == 0:
        return
    else:
        proxy_url = input("input proxy address if needed, press Enter if not:")
        if len(proxy_url) != 0:
            set_proxy(proxy_url)
        for url in galleries:
            gallery_id = ""
            for s in url.replace('?', '/').split('/'):
                if s.isdigit():
                    gallery_id = s
                    break
            if len(gallery_id) == 0:
                print("illegal gallery url:", url)
                continue
            url = url + f"?gid={gallery_id}&view=2"
            get_html(url, gallery_id)


def get_html(url, gallery_id):
    print(f"connecting to {url}")
    try:
        html = urllib.request.urlopen(url).read()
    except Exception as e:
        print(f"failed to access to {url}: {e}")
        time.sleep(random.uniform(1, 3))
        return
    gallery_name = re.search(r'<title>(.*?)</title>', html.decode('utf-8')).group(1)
    print("processing gallery:", gallery_name)
    get_image_urls(html, gallery_id, gallery_name)


def get_image_urls(html, gallery_id, gallery_name):
    pic_ids = re.findall('<td id="([0-9]+)" align="center"  valign="top">', html.decode('utf-8'))
    urls = []
    for i, pic_id in enumerate(pic_ids):
        url = "http://www.imagefap.com/photo/{0}/?pgid=&gid={1}&page=0".format(pic_id, gallery_id)
        html = urllib.request.urlopen(url).read()
        print(f"getting url of the {i + 1}th pic, total {len(pic_ids)}")
        while 1:
            a = re.findall('<a href=("https://cdnc*.imagefap.com/images/full/.*?{0}.*?")'.format(re.escape(pic_id)),
                           html.decode('utf-8'))
            if len(a) == 0:
                print(html)
                print(id)
                return
            elif len(re.findall('<a href', a[0])) == 0:
                urls.append(a[0][1:-1])
                break
            else:
                html = a[0]
        time.sleep(random.uniform(1, 3))
    download_pics(urls, gallery_name)


def download_pics(urls, gallery_name):
    try:
        os.mkdir(gallery_name)
    except Exception as e:
        print(repr(e))
    for i, url in enumerate(urls):
        print(f"downloading the {i + 1}th pic, total {len(urls)}")
        pic = str(i + 1) + '.jpg'
        urllib.request.urlretrieve(url, pic)
        new_path = os.path.join(gallery_name, pic)
        os.rename(pic, new_path)
        time.sleep(random.uniform(1, 3))

def set_proxy(addr):
    proxies = {
        'https': addr,
        'http': addr
    }
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    urllib.request.install_opener(opener)

if __name__ == "__main__":
    main()

