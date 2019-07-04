from bs4 import BeautifulSoup as BS
from bs4.element import Tag
import requests
import pickle
import os
import time
import re

def mkdir(dirname):
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass


sillok_list =  ['kaa', 'kba', 'kca', 'kda', 'kea', 'kfa', 'kga', 'kha', \
                'kia', 'kja', 'kka', 'kla', 'kma', 'kna', 'knb', 'koa', \
                'kob', 'kpa', 'kqa', 'kra', 'krb', 'ksa', 'ksb', 'kta', \
                    'ktb', 'kua', 'kva', 'kwa', 'kxa', 'kya']

mons_addr = 'http://sillok.history.go.kr/search/inspectionMonthList.do?id='
days_addr = 'http://sillok.history.go.kr/search/inspectionDayList.do?id='
arti_addr = 'http://sillok.history.go.kr/id/'
def crawl_articlelist(sillok_id):
    req = requests.get(mons_addr + sillok_id)
    soup = BS(req.text, 'html.parser')
    # get month links from each sillok page
    def check_monlink(href):
        return href and re.compile("\'k\w\w_\d\d\d\d\d\d\'").search(href)
    monlinks = soup.find_all(href=check_monlink)
    monlist = []
    for monlink in monlinks:
        monlist.append(str(monlink['href'])[19:29])
    # get each article links from month page
    def check_daylink(href):
        return href and re.compile("\'k\w\w_\d\d\d\d\d\d\d\d_\d\d\d\'").search(href)
    daylist = []
    count = 0
    for mon in monlist:
        req = requests.get(days_addr + mon)
        soup = BS(req.text, 'html.parser')
        daylinks = soup.find_all(href=check_daylink)
        for daylink in daylinks:
            dayitem = str(daylink['href'])[23:39]
            daylist.append(dayitem)
        count += 1
        print('crawled', count, '/', len(monlist))
        time.sleep(0.1)
    return daylist

def write_articlelist(sillok_id, articlelist):
    f = open('sillok/' + sillok_id, 'w')
    for item in articlelist:
        f.write(item + '\n')
    f.close()

def write_all_articlelist():
    mkdir('sillok')
    for sillok in sillok_list:
        print('sillok', sillok)
        l = crawl_articlelist(sillok)
        write_articlelist(sillok, l)

# write_all_articlelist()

def crawl_article(article_id):
    req = requests.get('http://sillok.history.go.kr/id/' + article_id)
    soup = BS(req.text, 'html.parser')
    raw = soup.find_all('div', {'class': 'ins_view_pd'})
    return (article_id, str(raw[0]), str(raw[1]))

def crawl_dump(filename, data):
    pickle.dump(data, open('raw/' + filename, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

def crawl_all_articles():
    mkdir('raw')
    filenames = os.listdir('sillok')
    for filename in filenames:
        with open('sillok/' + filename, 'r') as f:
            print('crawling', filename)
            lines = list(dict.fromkeys(f.readlines()))
            lines.sort()
            current_mon = lines[0][0:9]
            data = []
            for line in lines:
                if current_mon != line[0:9]:
                    crawl_dump(current_mon, data)
                    print('crawled', current_mon)
                    data.clear()
                    current_mon = line[0:9]
                data.append(crawl_article(line.strip()))
                time.sleep(0.1)
            crawl_dump(current_mon, data)
        
crawl_all_articles()

