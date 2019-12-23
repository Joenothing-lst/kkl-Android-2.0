# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'plus'))
import nonebot
from nonebot import on_command, CommandSession, Message, permission as perm
from random import choice,randint
import re
import wenda
from aiocqhttp.exceptions import ActionFailed

bot = nonebot.get_bot()
master = bot.config.MASTER
first=True
bangroup=[]#推送屏蔽群名单

@on_command('send_group_list', aliases=('群信息',))
async def send_group_list(session: CommandSession):
    message_type=session.ctx['message_type'] 
    user_id=session.ctx['user_id']
    #判断发送的消息是私聊的，并且判断发送者的qq号码
    if message_type=='private' and user_id in master:
        #获取qq群的信息
        try:
            group_list = await session.bot.get_group_list()
        except ActionFailed as e:
            print(e.retcode)
        msg='一共有{}个群：'.format(len(group_list))
        for group in group_list:
            msg+='\n-----------------\n'+'群名称:' + group['group_name'] + '\n' +'群号:' + str(group['group_id'])
        await session.bot.send_private_msg(user_id=master[0],message=msg)

@on_command('test', only_to_me=True)
async def ts(session: CommandSession):
    await session.send(message=str(session.ctx))

@bot.on_message('private')
async def private_wenda_update(context):
    f_message = context['raw_message'].strip()
    f_user_id = context['user_id']
    msg=wenda.reply(f_message,f_user_id)
    if msg:
        await bot.send_private_msg(user_id=f_user_id, message=msg)

    if f_user_id in master:
        if '删除全局词条' in f_message :
            await bot.send_private_msg(user_id=f_user_id, message=wenda.delet(f_message,1))

        if '问' in f_message and '答' in f_message and '问答' not in f_message:
            if '全局问' in f_message and f_user_id in master:
                await bot.send_private_msg(user_id=f_user_id, message=wenda.add(f_message,1))
            else:
                await bot.send_private_msg(user_id=f_user_id, message=wenda.add(f_message,f_user_id))

        if f_message == '读取词库':
            await bot.send_private_msg(user_id=f_user_id, message=wenda.readdir())

@bot.on_message('group')
async def group_wenda_main(context):
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    global first
    if first:
        wenda.readdir()
        print('\n可可萝启动，记忆装载完毕\n')
        first = False
#词库开始工作
    msg=wenda.reply(f_message,f_group_id)
    if msg:
        await bot.send_group_msg(group_id=f_group_id,message=msg)

#群指令
@bot.on_message('group')
async def group_ban(context):
    f_message = context['raw_message'].strip()
    f_group_id = context['group_id']
    f_user_id = context['user_id']
    f_self_id = context['self_id']
    try:
        group_memberinfo = await bot.get_group_member_list(group_id=f_group_id)
        f_manager=[i['user_id'] for i in group_memberinfo if i['role']=='owner' or i['role']=='admin']

        if f_user_id in f_manager:
            if '删除词条' in f_message :
                await bot.send_group_msg(group_id=f_group_id, message=wenda.delet(f_message,f_group_id))

            if '问' in f_message and '答' in f_message and '问答' not in f_message:
                if '全局问' in f_message and f_user_id in master:
                    await bot.send_group_msg(group_id=f_group_id, message=wenda.add(f_message,1))
                else:
                    await bot.send_group_msg(group_id=f_group_id, message=wenda.add(f_message,f_group_id))

            if f_message == '读取词库':
                await bot.send_group_msg(group_id=f_group_id, message=wenda.readdir())

        if '抽' in f_message and '奖' in f_message or '一带一路' in f_message or '解除禁言' in f_message:
            if f_self_id in f_manager:
                if f_user_id not in f_manager and '抽' in f_message and '奖' in f_message and '一带一路' not in f_message:
                    little = randint(120,480)
                    large = randint(12000,25000)
                    if '大' in f_message or '带' in f_message:
                        await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=large)
                    else:
                        await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=little)

                elif f_user_id not in f_manager and '[CQ:at,qq=' in f_message and 'all' not in f_message and '一带一路' in f_message:
                    p = 'CQ:at,qq=(\\d+)]'
                    qq = int(re.search(p,f_message).group(1))
                    if f_user_id not in f_manager and qq not in f_manager:
                        bantime = randint(120,480)
                        await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=bantime + randint(-60,180))
                        await bot.set_group_ban( group_id=f_group_id, user_id=qq, duration=bantime)
                        await bot.send_group_msg( group_id=f_group_id, message=f'恭喜[CQ:at,qq={f_user_id}]成功带动了[CQ:at,qq={qq}]的经济发展')
                    elif f_user_id not in f_manager and qq in f_manager:
                        await bot.send_group_msg( group_id=f_group_id, message=f'[CQ:at,qq={f_user_id}] 你的行动失败了，没有符合帮扶政策的群员，你将独享')
                        await bot.set_group_ban( group_id=f_group_id, user_id=f_user_id, duration=randint(120,480))

                elif '解除禁言' in f_message and '[CQ:at,qq=' in f_message and 'all' not in f_message:
                    if f_user_id in f_manager:
                        p = 'CQ:at,qq=(\\d+)]'
                        qq = int(re.search(p,f_message).group(1))
                        await bot.set_group_ban( group_id=f_group_id, user_id=qq, duration=0)
                    else:
                        await bot.send_group_msg( group_id=f_group_id, message='这是管理权限哦')
                else:
                    await bot.send_group_msg(group_id=f_group_id, message='权限狗无法参与(自裁吧')
            else:
                await bot.send_group_msg( group_id=f_group_id, message='可可萝不是管理员哦')

        if '晚安' in f_message:
            if f_user_id in master:
                await bot.send_group_msg( group_id=f_group_id, message=f'[CQ:at,qq={f_user_id}] 晚安，主人~ mua~')
            else :
                await bot.send_group_msg( group_id=f_group_id, message=f'[CQ:at,qq={f_user_id}] 晚安，骑士君~')
        elif '妈' in f_message :
            f=True
            for i in ['狗','你','的','他','草','呀','查询']:
                if i in f_message:
                    f=False
            if f:
                await bot.send_group_msg( group_id=f_group_id, message=f'[CQ:at,qq={f_user_id}] ？')
    except :
        pass

@on_command('unset_ban', aliases=('大赦天下','大赦天下！'), only_to_me=False)
async def unset_ban(session: CommandSession):
    f_group_id=session.ctx['group_id']
    group_memberinfo = await bot.get_group_member_list(group_id=f_group_id)
    f_manager=[i['user_id'] for i in group_memberinfo if i['role']=='owner' or i['role']=='admin']
    if session.ctx['message_type'] == 'group' and session.ctx['user_id'] in f_manager and len(group_memberinfo) <= 100:#成员小于100人
        for m in group_memberinfo:
            await bot.set_group_ban( group_id=f_group_id, user_id=m['user_id'], duration=0)

@on_command('send_all_group', aliases=('公告','群发','推送',), only_to_me=False)
async def send_all_group(session: CommandSession):
    if session.ctx['user_id'] in master:
        msg=session.current_arg.strip()
        if not msg:
            msg = session.get('message', prompt='准备完成')
        group_list = await session.bot.get_group_list()
        for group in group_list:
            if group['group_id'] not in bangroup:
                try:
                    await bot.send_group_msg( group_id=group['group_id'], message=msg)
                except:
                    pass
        await session.send('推送完成')
