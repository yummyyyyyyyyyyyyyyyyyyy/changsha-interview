import requests

cookies = {
    'Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0': '1789195661,1789207509',
    'HMACCOUNT': '3474ED5770D60F8F',
    'sessionid': 'utiarl0r3ntdm8s6at420ka7pjxlf13v',
    'Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0': '1789208383',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://match.yuanrenxue.cn/match/19',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0=1789195661,1789207509; HMACCOUNT=3474ED5770D60F8F; sessionid=utiarl0r3ntdm8s6at420ka7pjxlf13v; Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0=1789208383',
}

params = {
    'pageSize': '10',
    'kw': '',
}

numbers = []
for page in range(1, 6):
    params['page'] = str(page)
    if page == 5:
        headers['user-agent'] = 'yuanrenxue'
    response = requests.get('https://match.yuanrenxue.cn/api/question/19', params=params, cookies=cookies, headers=headers)
    data = response.json()['data']
    numbers += data
    print('第%d页:' % page, data)

# print('全部数字:', numbers)
print('相加结果:', sum(numbers))