# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession, permission as perm
import nonebot
import random as rd
from PIL import Image
import os
root=os.path.join(os.path.dirname(__file__),'plus','image')
os.chdir(root)
bot=nonebot.get_bot()
master = bot.config.MASTER[0]

gacya3 = ['中二.png',
        '狐狸.png',
        '妹弓.png',
        '初音.png',
        '霞.png',
        '魅魔.png',
        '充电宝.png',
        '偶像.png',
        '扇子.png',
        '哈哈剑.png',
        'xcw.png',
        'tomo.png',
        '狼.png',
        '伊利亚.png',
        '黑骑.png',
        '姐姐.png',
        '莫妮卡.png',
        '流夏.png',
        '吉他.png',
        '亚里莎.png',
        '安.png',
        '龙姬.png',
        '江户抖m.png',
        '江户扇子.png']

gacya2 = ['跳跳虎.png',
        '妹法.png',
        '布丁.png',
        '镜子.png',
        '七七香.png',
        '圣母.png',
        '暴击弓.png',
        '狗.png',
        '兔子.png',
        '熊锤.png',
        '松鼠.png',
        '病娇.png',
        '忍.png',
        '奶牛.png',
        'tp弓.png',
        '千歌.png',
        '抖m.png',
        '猫剑.png',
        '子龙.png',
        '眼罩.png',
        '裁缝.png']

gacya1 = ['猫拳.png',
        '优衣.png',
        '剑圣.png',
        '炸弹人.png',
        '铃铛.png',
        '姐法.png',
        '女仆.png',
        '黄骑.png',
        '香菜.png',
        '大眼.png',
        '羊驼.png',
        '路人.png']

fesgacya = ['克总.png',
        '511.png']

up = ['水狐狸.png']
fes = '0'
isdouble = '0'
background = Image.new('RGBA',(330,135),color='lavenderblush')
#up,3星,2星,1星
ordinary=[0.7,1.8,20.5,77]#普通
double=[1.4,3.6,18,77]#双倍

#gacya
@on_command('gacya10', aliases=('十连抽',), only_to_me=False)                 #changed
async def gacya(session: CommandSession):
    gacya_3= gacya3
    result = []
    msg=''
    p=ordinary
    sup,s3,s2=100-p[0],100-p[0]-p[1],p[3]
    if session.ctx['message_type'] == 'group':
        msg = '[CQ:at,qq={}]\n'.format(str(session.ctx['user_id']))
    if fes=='1':
        p=double
        gacya_3+=fesgacya
    if isdouble=='1':
        p=double
    for n in range(9):
        i = rd.random()*100
        if i >= sup:                     #up
            result.append(rd.choice(up))
        elif i >= s3 and i < sup:       #3星
            result.append(rd.choice(gacya_3))
        elif i >= s2 and i < s3:       #2星
            result.append(rd.choice(gacya2))
        else :                           #1星
            result.append(rd.choice(gacya1))
    result.append(rd.choice(gacya2)) if (rd.random()*100 < s3) else result.append(rd.choice(gacya_3+up))

    name=session.ctx['user_id']
    a=0
    for x in range(5):
        for y in range(2):
            pic=Image.open(result[a])

            background.paste(pic,(x*65+5,y*65+5))
            a+=1
    background.save(root+f'\\out\\{name}.png')
    await session.send(msg+f'[CQ:image,file=file:///{root}\\out\\{name}.png]')

@on_command('set_gacya',aliases=('设置',),only_to_me=False)
async def set_gacya(session:CommandSession):
    global fes,isdouble
    if master == session.ctx['user_id']:
        msg=session.current_arg_text.strip()
        if not msg:
            msg = session.get('message', prompt='准备完成')
        fes=msg[0]
        try:
            isdouble=msg[1]
        except:
            isdouble='0'
        await session.send(message=f'设置完成,现在卡池设置\nfes：{fes}\n双倍：{isdouble}')

