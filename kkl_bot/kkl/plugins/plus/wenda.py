# -*- coding:utf-8 -*-
import os
import re
import json
root=os.path.join(os.path.dirname(__file__),'kkl_dictionary.json')
a={1:{}}
#保存词库方法
def savedir(msg):
    global a
    with open(root,'w',encoding='utf-8') as file:
        json.dump(msg, file, ensure_ascii=False)
    return '已保存~'
#读取词库方法
def readdir():
    global a
    with open(root,'r',encoding='utf-8') as file:
        a=json.load(file)
    return '已读取~'
#存词条方法
def add(msg,id):
    global a
    id=str(id)
    p='问(.*?)答(.+)'
    msg=re.findall(p,msg)[0]
    if id in a:
        a[id][msg[0]]=msg[1]
    else:
        a[id]={msg[0]:msg[1]}
    savedir(a)
    return '可可萝记住了~'
#删除词条方法
def delet(msg,id):
    global a
    id=str(id)
    msg=re.findall('词条(.+)',msg)[0]
    try:
        if (msg in [i for i in a['1']]) and (msg not in [i for i in a[id]]):
            return '你没有权限修改全局词条哦~'
        del a[id][msg]
        savedir(a)
        return '已删除~'
    except:
        return '可可萝不知道这个词哦~'
#响应方法
def reply(msg,id):
    id=str(id)
    if '删除' not in msg:
        #判断有无词典,优先级高于全局
        if id in a:
            for i in a[id]:
                if i in msg:
                    return a[id][i]
        #判断是否全局
        for i in a['1']:
            if i in msg:
                return a['1'][i]
