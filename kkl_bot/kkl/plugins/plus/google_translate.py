# -*- coding:utf-8 -*-
import re
import requests
import demjson

from pprint import pformat, pprint
from urllib.parse import urlencode
from encryption import mr

session = requests.session()


def translate(q='hello', source='en', to='zh-CN', tkk=None):
    """
    限制最大5000,按utf-8算，一个汉字算1个,1个英文算一个，超过会失败
    """
    if not tkk:
        tkk = '426151.3141811846'
    tk = mr(q, tkk)
    params = {
        'client': 't',
        'sl': source,
        'tl': to,
        'hl': source,
        'dt': [
            'at', 'qca', 'rw', 'rm', 'ss', 't'
            ],
        'tk': tk,
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'pc': 1,
        'kc': 1,
        'ssel': 0,
        'otf': 1
    }
    data = {
        'q': q
    }
    headers = {
        'Referer': 'https://translate.google.cn/',
        'Host': 'translate.google.cn',
    }
    resp = requests.post('https://translate.google.cn/translate_a/single', params=params, data=data, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        data = resp.json()
        
        result = []
        result.append(''.join(map(lambda x:x[0], data[0][:-1])))
        result.append(data[0][-1][-1])
        return result
    else:
        return None


def ref_words(q='hello', source='en', to='zh-CN'):
    """没啥JB用处"""
    params = {
        'q': q,
        'client': 'translate-web',
        'ds': 'translate',
        'hl': source,
        'requiredfields': f'tl:{to}',
        'callback':'window.google.ref_words'
    }
    url = 'https://clients1.google.com/complete/search?'
    headers = {
        'Referer': 'https://translate.google.cn/',
        'Host': 'clients1.google.cn',
    }
    resp = session.get(url, params=params, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        result = re.search(r'window.google.ref_words\((.*)\)', resp.text).group(1)
        json_data = demjson.decode(result)
        data_list = list(map(lambda x:x[0], json_data[1]))
        return data_list
    else:
        return None