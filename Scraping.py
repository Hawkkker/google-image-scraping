from selenium import webdriver
from sys import argv
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote
import urllib.request
import os
import re
import argparse
import sys

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", help="get only link of image", action="store_true")
    parser.add_argument("keywords", help="keywords")
    args = parser.parse_args()
    link = 0
    if args.link:
        link = 1
    browser = webdriver.Chrome()
    browser.get("https://www.google.com/?tbm=isch")
    search = browser.find_element_by_name('q')
    search.clear()
    search.send_keys(args.keywords, Keys.ENTER)
    elem1 = browser.find_element_by_id('islrg')
    click = elem1.find_elements_by_tag_name("a")
    click[0].click()
    url_pattern = r"imgurl=\S*&amp;imgrefurl"
    image_element = browser.find_element_by_class_name("islib")
    outer_html = image_element.get_attribute("outerHTML")
    re_group = re.search(url_pattern, outer_html)
    while re_group is None:
        re_group = re.search(url_pattern, outer_html)
    image_url = unquote(re_group.group()[7:-14])
    try:
        os.mkdir('downloads')
    except FileExistsError:
        pass
    src = image_url
    try:
        if src != None:
            src  = str(src)
            if link == 0:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(src, os.path.join('downloads', args.keywords + '.jpg'))
                out = os.path.join('./downloads/', args.keywords + '.jpg')
            else:
                out = src
        else:
            raise TypeError
    except TypeError:
        print('fail')
    print(out)
    browser.quit()

if __name__ == '__main__':
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()