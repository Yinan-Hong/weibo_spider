base_url = 'https://m.weibo.cn/detail/'
url = 'https://m.weibo.cn/comments/hotflow?id='


Cookie = {
    'Cookie': '填入你的cookie' # 这里要填
}

headers = {
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': '填入你的token', # 这里要填
    'Accept': 'application/json, text/plain, */*'
}


# 数据id号，要爬取的微博的id号
weiboComment = [{
    'id':1,
    'weibo_id': '填入你的id', # 这里要填
}]