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
    #sub = elem1.find_elements_by_tag_name('img')
    click = elem1.find_elements_by_tag_name("a")
    click[0].click()
    url_pattern = r"imgurl=\S*&amp;imgrefurl"
    image_element = browser.find_element_by_class_name("islib")
    outer_html = image_element.get_attribute("outerHTML")
    re_group = re.search(url_pattern, outer_html)
    while re_group is None:
        re_group = re.search(url_pattern, outer_html)
    image_url = unquote(re_group.group()[7:-14])
    #elem2 = browser.find_element_by_id('Sva75c')
    #soup = BeautifulSoup(browser.page_source)
    #sub = elem2.find_elements_by_xpath('img.n3VNCb')
    try:
        os.mkdir('downloads')
    except FileExistsError:
        pass
    #print(sub)#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div.OUZ5W > div.zjoqD > div > div.v4dQwb > a > img   n3VNCb '.n3VNCb'
    #print (len(sub))
    ##src = sub[0].get_attribute('src')
    src = image_url
    #data = src.split(',', 1)
    #print(data[1])
    #f = open("myfile.txt", "x")
    #f.write(data[1])
    #ext = re.search('/(.+?);', data[0]).group(1)
    #base64_string = src
    #decoded_string = base64.b64decode(data[1])
    try:
        if src != None:
            src  = str(src)
            if link == 0:
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