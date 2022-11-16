from urllib.request import urlopen
import re

ignore_list = ["无宠","已租", "限男生", "admin", "付费置顶广告？", "万人大群", "share","公用卫生间", "不允许养宠物"]

def read_page(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def read_title_page(i):
    link = f"http://bay123.com/forum-40-{i}.html"
    contents = read_page(link)
    all_links = re.findall(r'thread-.*-.*-.*\.html\"', contents)
    all_links = set(all_links)
    valid_url = []
    for url in all_links:
        link = url.split('"')
        valid_url.append(link[0])
    return valid_url

def allow_pet(threadid):
    url = 'http://bay123.com/' + threadid
    contents = read_page(url)
    for ig in ignore_list:
        if ig in contents:
            return False
    price = re.findall('\$[0-9]*', contents)
    pri = [int(x[1:]) for x in price if len(x) > 1]
    for np in pri:
        if np >= 1400:
            return False
    return True

def filter_one_page(pageid):
    one_page = []
    all_thread = read_title_page(pageid)
    for thread in all_thread:
        allow = allow_pet(thread)
        if allow:
            one_page.append(thread)
    return one_page

def filter_page_range(page_ran=30):
    all_allow = []
    for i in range(1, page_ran):
        all_allow.extend(filter_one_page(i))
    return all_allow

def save_search_res():
    all_allow = filter_page_range(15)
    print(len(all_allow))
    with open('all_pets.txt', 'w+') as file:
        for allow in all_allow:
            file.write(f'http://bay123.com/{allow}\n')

save_search_res()
#res = allow_pet('thread-142411-1-1.html')
#print(str(res))
#print(res)
