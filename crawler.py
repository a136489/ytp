#-*- coding: UTF-8 -*- 
import requests
import os
import urllib
import pandas as pd
from IPython.display import Image, HTML, display
from lxml import etree


def get_current_page_number():
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    res = requests.get(url)
    root = etree.fromstring(res.content, etree.HTMLParser())
    
    prev_page_link = root.xpath('//div[@class="action-bar"]/div[2]/a[2]/@href')[0]
    return int(prev_page_link[prev_page_link.find('index')+5:prev_page_link.find('.html')]) + 1

# get all photos of an artical
def get_one_page(url, lowest):
    urllist = {}
    
    res = requests.get(url)
    res.encoding = 'utf-8'
    
    root = etree.fromstring(res.content, etree.HTMLParser())
    
    push_num_select = '//div[@class="r-ent"][div[@class="title"]/a/text() != 0]/div[@class="nrec"]/span/text()'
    title_select = '//div[@class="r-ent"][div[@class="nrec"]/span/text() != 0]/div[@class="title"]/a/text()'
    link_select = '//div[@class="r-ent"][div[@class="nrec"]/span/text() != 0]/div[@class="title"]/a/@href'

    for push, title, link in zip(root.xpath(push_num_select), root.xpath(title_select), root.xpath(link_select)):
        if (push.isdigit() and int(push) >= lowest) or (~push.isdigit() and push == u'爆'):
            if title[1:3] != u'公告':
                urllist[u'('+push+u') '+title] = [link]
            
    imgData = {}
    for i in urllist:
        imgData[i] = []
        turl = 'https://www.ptt.cc' + urllist[i][0]
        print turl
        tres = requests.get(turl)
        
        troot = etree.fromstring(tres.content, etree.HTMLParser())
        
        x = [str(src) for src in troot.xpath('//div[@class="richcontent"]/img/@src')]
        urllist[i].append(x)
    for i in urllist:
#         if you don't have this album
        try:
            os.mkdir(i.encode('utf-8'))
            for img in urllist[i][1]:
                urllib.urlretrieve('http:%s' % img, '%s/%s' %(i, urllist[i][1].index(img)))
                display(HTML('<img src="http:%s">' % img))
#         if you already have this album
        except:
            for img in urllist[i][1]:
                display(HTML('<img src="http:%s">' % img))


def get_Beauty(page_range, lowest):
    current_page_number = get_current_page_number()
#     get photo from page N-k to page N. N and K represents current(latest) page and the number of page you want respectively 
    for i in range(current_page_number, current_page_number-page_range, -1):
        print i
        current_page = 'https://www.ptt.cc/bbs/Beauty/index' + str(i) + '.html'
        get_one_page(current_page, lowest)

# getBeauty(page_number, push_lowest_bound)
get_Beauty(2, 50)
