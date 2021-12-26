import requests
import time
from config import headers, url, Cookie, base_url, weiboComment
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
        # 删除评论文本中的html格式表情符号
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
    with open(txt_name, mode='w', encoding='utf-8') as file_handle:
        for obj in commentLists:
            file_handle.write(obj['comment_text'] + '\n')


# 爬取第一页的微博评论
def first_page_comment(weibo_id, url, headers):
    global commentLists
    try:
        url = url + str(weibo_id) + '&mid=' + str(weibo_id) + '&max_id_type=0'
        web_data = requests.get(url, headers=headers,
                                cookies=Cookie, timeout=20)
        js_con = web_data.json()
        max_id = js_con['data']['max_id']
        max = js_con['data']['max']
        comments_list = js_con['data']['data']
        extract_data(comments_list)

        write_in('1-1')

        print("已获取第1页的评论")
        return max_id, max, commentLists

    except Exception as e:
        print("遇到异常")


# 爬取剩余页面的评论
def get_rest_comments(count, weibo_id, url, headers, max, urlNew):
    global commentLists
    last = count  # 记录写入磁盘的页数

    while count <= max:
        # 避免被反爬
        time.sleep(0.8+random.random())
        try:
            web_data = requests.get(
                url=urlNew, headers=headers, cookies=Cookie, timeout=10)

            # get请求成功
            if web_data.status_code == 200:
                js_con = web_data.json()

                if js_con['ok'] == 1:
                    # 提取数据
                    max_id = js_con['data']['max_id']
                    comments_list = js_con['data']['data']
                    max_id_type = js_con['data']['max_id_type']
                    extract_data(comments_list)

                    print("已获取第" + str(count) + "页的评论。")
                    count += 1
                    # 得到下一页的url
                    urlNew = url + str(weibo_id) + '&mid=' + str(weibo_id) + \
                        '&max_id=' + str(max_id) + \
                        '&max_id_type=' + str(max_id_type)

            else:
                raise Exception('Request Error')

            # 每500页写入一下txt
            if count % 500 == 0:
                # 格式化txt文件名称：wlh_{起始页}-{终止页}.txt
                index = str(last) + '-' + str(count)
                last = count + 1
                write_in(index)
                # 清空前面的数据
                commentLists = []
                # 记录一下当前的url，以免出错后要从头开始爬
                with open('log.txt', 'a') as log:
                    msg = '\nMark\n' + urlNew + '\ncnt = ' + str(count) + '\n'
                    log.write(msg)

        except Exception as e:

            e_msg = e.__str__()

            # 出现异常时保存当前读到的页数和url
            with open('log.txt', 'a') as log:
                msg = 'Error\n' + urlNew+'\ncnt = ' + str(count) + '\n'
                log.write(msg)+'\n'
                log.write(e_msg+'\n')

            # 把截至当前页数的数据写入磁盘
            index = str(last) + '-' + str(count)
            write_in(index)

            if e_msg[:5] == 'HTTPS':
                continue
            break


commentLists = []  # 初始化存储一个微博评论数组

if __name__ == "__main__":
    weibo_comment = weiboComment

    # 存储每一篇微博的评论数据
    for ind, item in enumerate(weibo_comment):
        # 爬取第一页评论
        max_id, max_page, output = first_page_comment(
            item['weibo_id'], url, headers)

        if len(output) > 0:
            # 如果结果不只一页，就继续爬
            if(max_page != 1):
                urlNew = url + str(item['weibo_id']) + '&mid=' + str(item['weibo_id']) + \
                    '&max_id=' + str(max_id) + '&max_id_type=0'

                get_rest_comments(2, item['weibo_id'],
                                  url, headers, max_page, urlNew)

            else:
                print('----------------该微博的评论只有1页-----------------')
