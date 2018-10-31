from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Cookie': 'img_check_token=fe2d010308a6b3799a3d9c728ee74244; pgv_pvi=5490903040; pgv_si=s4538757120; pgv_info=ssid=s2817565190; ts_refer=www.google.com.hk/; pgv_pvid=2768947008; ts_uid=1092662959; pc_userinfo_cookie=; ts_last=ac.qq.com/Comic/all/search/time/page/1',
    'Connection': 'keep-alive',
    'Host': 'ac.qq.com',
    'Referer': 'http://ac.qq.com/',
    'Upgrade-Insecure-Requests': '1'

}


def html_find():
    conn = MongoClient("localhost",27017)
    db = conn.stu
    myset = db.pinkmanhua
    urls = ['http://ac.qq.com/Comic/all/search/time/page/{}'.format(n) for n in range(1, 101)]
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
            img = i.find('img', class_='lazy').get('data-original')  #图片链接
            author = i.find('p', class_='ret-works-author').get('title')#作者
            tag = i.find('p', class_="ret-works-tags").text
            mid = tag.split()
            tags = mid[:-1]#标签
            #decs = i.find('p', class_="ret-works-decs")#简介
            span = i.find('span', class_="mod-cover-list-text")#更新进度
            href = i.find('a').get('href')  # 引申连接
            ll = 'http://ac.qq.com'
            hrefs = ll + href

            req = requests.get(hrefs, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            over = soup.find('div', class_="ui-left works-intro-wr")
            up = over.find('div', class_="works-intro clearfix")
            down = over.find('div', class_="works-vote clearfix")
            decs = up.find('p',class_="works-intro-short ui-text-gray9")#简介
            grade = up.find('p', class_="ui-left").text  # 分数
            ticket = down.find('strong', id="redcount").text  # 红票
            hot = up.find('p',class_="works-intro-digi").text
            hotss = re.findall('[0-9]+.',hot)[:-1]#热度，正则表达式

            ticketss = re.findall('[0-9]+',ticket)
            gradess = re.findall("[0-9]+.[0-9]+", grade)[:1]
            grades = ''.join(gradess)#转换为字符串
            tickets = ''.join(ticketss)
            hots = ''.join(hotss)

            data = {
                '标题': title,
                '图片链接': img,
                '作者': author,
                '标签': tags,
                '热度': hots ,
                '简介': str(decs.text).strip(),
                '更新进度': span.text,
                '分数':grades ,
                '红票数':tickets

            }
            pprint(data)
            myset.insert(data)


html_find()
