import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import json

import execjs
import requests

data_url = 'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/project/list?pg=%s&pgsz=15&total=450'


def get_encrypted_data(page):
    headers = {
        'Host': 'jzsc.mohurd.gov.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'timeout': '30000',
        'accessToken': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://jzsc.mohurd.gov.cn/data/project',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1681920842; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1681933793',
    }
    encrypted_data = requests.get(url=data_url % page, headers=headers).text
    return encrypted_data


def get_decrypted_data(encrypted_data):
    with open('req_aes.js', 'r', encoding='utf-8') as f:
        jzsc_mohurd_js = f.read()
    decrypted_data = execjs.compile(jzsc_mohurd_js).call('getDecryptedData', encrypted_data)
    return json.loads(decrypted_data)


def main():
    # 10页数据
    for page in range(10):
        encrypted_data = get_encrypted_data(page)
        decrypted_data = get_decrypted_data(encrypted_data)
        print(decrypted_data)


if __name__ == '__main__':
    main()
