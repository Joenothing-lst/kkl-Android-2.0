# -*- coding:utf-8 -*-
from datetime import datetime
import nonebot

bot = nonebot.get_bot()
#使用计划任务模块之前请在命令行执行pip install nonebot[scheduler]
#可自行添加不发送定时消息的群列表

@nonebot.scheduler.scheduled_job('cron', hour='14', minute='50', second='0', misfire_grace_time=60) # = UTC+8 1445
async def pcr_reminder():
    try:
        group_list = await bot.get_group_list()
        msg = '背刺Time背刺Time背刺Time背刺Time背刺Time!!!'
        groups = [group['group_id'] for group in group_list]
        for group in groups:
            await bot.send_group_msg(group_id=group, message=msg)
    except:
        pass


@nonebot.scheduler.scheduled_job('cron', hour='8', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def alarm():
    try:
        group_list = await bot.get_group_list()
        msg = '起床啦!!!'
        groups = [group['group_id'] for group in group_list]
        for group in groups:
            await bot.send_group_msg(group_id=group, message=msg)
    except:
        pass

@nonebot.scheduler.scheduled_job('cron', hour='23', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def need_sleep():
    try:
        group_list = await bot.get_group_list()
        msg = '现在23点，骑士君该睡觉了！'
        groups = [group['group_id'] for group in group_list]
        for group in groups:
            await bot.send_group_msg(group_id=group, message=msg)
    except:
        pass

