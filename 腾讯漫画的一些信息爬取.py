from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
from pymongo import MongoClient




headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Cookie': 'img_check_token=fe2d010308a6b3799a3d9c728ee74244; pgv_pvi=5490903040; pgv_si=s4538757120; pgv_info=ssid=s2817565190; ts_refer=www.google.com.hk/; pgv_pvid=2768947008; ts_uid=1092662959; pc_userinfo_cookie=; ts_last=ac.qq.com/Comic/all/search/time/page/1',
    'Connection': 'keep-alive',
    'Host': 'ac.qq.com',
    'Referer': 'http://ac.qq.com/',
    'Upgrade-Insecure-Requests': '1'

}


def html_find():
    conn = MongoClient("localhost",27017)#连接数据库
    db = conn.stu
    myset = db.pppinkmanhua#创建集合
    urls = ['http://ac.qq.com/Comic/index/state/pink/page/{}'.format(n) for n in range(1, 142)]
    for url in urls:
         print(url)
         nan_data = requests.get(url, headers=headers)
         soup = BeautifulSoup(nan_data.text, 'lxml')
         time.sleep(1)
         ul = soup.find('div', class_="ret-main-wr ui-mb40 ui-left").\
            find('div', class_="ret-search-result").find('ul',class_="ret-search-list clearfix")
         whole = ul.find_all('li', class_="ret-search-item clearfix")
         for i in whole:

             title = i.find('a').get('title')#标题
             img = i.find('img', class_='lazy').get('data-original')#图片链接
             author = i.find('p', class_='ret-works-author').get('title')#作者
             tag = i.find('p', class_="ret-works-tags").text
             mid = tag.split()
             tags = mid[:-1]#标签
             hot = i.find('p', class_="ret-works-tags").find('span').text.replace('人气：','')#热度
             decs = i.find('p', class_="ret-works-decs")#简介
             span = i.find('span', class_="mod-cover-list-text")#更新进度
             href = i.find('a').get('href')  # 引申连接
             ll = 'http://ac.qq.com'
             hrefs = ll + href

             req = requests.get(hrefs, headers=headers)
             soup = BeautifulSoup(req.text, 'lxml')
             over = soup.find('div', class_="ui-left works-intro-wr")
             up = over.find('div', class_="works-intro clearfix")
             down = over.find('div', class_="works-vote clearfix")
             grade = up.find('strong', class_="ui-text-orange").text  # 分数
             ticket = down.find('strong', id="redcount").text  # 红票


             data = {
                 '标题': title,
                 '图片链接': img,
                 '作者': author,
                 '标签': tags,
                 '热度': hot if hot is not None else None,
                 '简介': decs.text,
                 '更新进度': span.text,
                 '分数':grade if grade is not None else None,
                 '红票数':ticket

             }


             pprint(data)
             myset.insert(data)#存入数据库



html_find()
