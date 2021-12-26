import requests
import time
from config import headers, url, Cookie, base_url, weiboComment
import wlh_spider
import random
import re


# 将中国标准时间(Sat Mar 16 12:12:03 +0800 2019)转换成年月日
def formatTime(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    time_struct = time.strptime(time_string, from_format)
    times = time.strftime(to_format, time_struct)
    return times

# 提取json包中的数据


def extract_data(comments_list):
    global commentLists
    for commment_item in comments_list:
        pure_text = re.sub('<.*?>', '', commment_item['text'])
        Obj = {
            'commentor_id': commment_item['user']['id'],
            'commentor_name': commment_item['user']['screen_name'],
            'commentor_blog_url': commment_item['user']['profile_url'],
            'comment_id': commment_item['id'],
            'comment_text': pure_text,
            'create_time': formatTime(commment_item['created_at'], '%a %b %d %H:%M:%S +0800 %Y', '%Y-%m-%d %H:%M:%S'),
            'like_count': commment_item['like_count'],
            'reply_number': commment_item['total_number'],
        }
        commentLists.append(Obj)


def write_in(index: str):
    global commentLists
    txt_name = 'res/wlh_' + str(index) + '.txt'
    with open(txt_name, mode='w', encoding='utf-8') as file_handle:  # 打开txt文件
        for obj in commentLists:
            file_handle.write(obj['comment_text'] + '\n')


commentLists = []  # 初始化存储一个微博评论数组

if __name__ == "__main__":
    weibo_comment = weiboComment

    with open('log.txt', 'r') as f:
        lines = f.readlines()
        cnt = lines[-1]
        cnt = int(cnt[6:])
        urlNew = lines[-2][:-1]

    # 存储每一篇微博的评论数据
    for ind, item in enumerate(weibo_comment):
        web_data = requests.get(
            url=urlNew, headers=headers, cookies=Cookie, timeout=10)
        if web_data.status_code == 200:
            js_con = web_data.json()
        max_page = js_con['data']['max']

        wlh_spider.get_rest_comments(
            cnt, item['weibo_id'], url, headers, max_page, urlNew)
