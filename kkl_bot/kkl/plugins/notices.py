# -*- coding:utf-8 -*-
import nonebot
from nonebot import on_notice, NoticeSession, on_request, RequestSession, on_command, CommandSession
from aiocqhttp.exceptions import ActionFailed
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'plus'))
import kkl_config
master=kkl_config.master[0]
# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def increase(session: NoticeSession):
    # 发送欢迎消息
    q = session.ctx['user_id']
    me = session.ctx['self_id']
    # 判断新成员是否是自己
    if q==me:
        await session.send('在下是可可萝，今后请多指教呐')
    else:
        await session.send(f'欢迎新大佬 [CQ:at,qq={q}]')

@on_notice('group_decrease')
async def decrease(session: NoticeSession):
    # 发送消息
    q = str(session.ctx['user_id'])
    m = str(session.ctx['operator_id'])
    if m==q:
        inf=await bot.get_stranger_info(user_id=q)
        name=inf['nickname']
        await session.send(f'{name}({q}) 跑了')

bot=nonebot.get_bot()
request_flag=False
@on_request('group')
async def bot_request(session: RequestSession):
    global request_flag
    f_group= session.ctx['group_id']
    f_user= session.ctx['user_id']
    if session.ctx['sub_type']=='invite':
        if request_flag == False:
            await session.bot.send_private_msg(user_id=f_user,message=f'想邀请可可萝入群嘛？请先点击这里联系作者：\nhttps://wpa.qq.com/msgrd?v=3&amp;uin={master}&amp;site=qq&amp;menu=yes')
            await session.bot.send_private_msg(user_id=master,message=f'有新的群邀请:\n群：{f_group}\n邀请人：{f_user}\n已忽略')
        else :
            try:
                await session.approve()
            except ActionFailed as e:
                print(e.retcode)
            await session.bot.send_private_msg(user_id=master,message=f'有新的群邀请:\n群：{f_group}\n邀请人：{f_user}\n已同意')
            request_flag=False

@on_notice('friend_add')
async def friend_add(session: NoticeSession):
    f_user=session.ctx['user_id']
    await bot.send_private_msg(user_id=master,message=f'有人加我啦！\n{f_user}')


@on_command('set_request', aliases=('开启邀请',), only_to_me=True)
async def set_request(session: CommandSession):
    global request_flag
    if session.ctx['user_id']==master:
        request_flag=True
        await session.bot.send_private_msg(user_id=master,message='已开启')