import os
import subprocess
from PIL import Image
from .utils import set_sw
from .utils import unset_sw
from .utils import get_sw
from .utils import set_id
from .utils import set_default
from .utils import unset_id
from .utils import get_id
from .utils import get_bind
from .utils import get_role
from .utils import pic_data
from .getcard import get_card
from .getinfo import get_user_info
from .getdetail import get_course_detail
from .getinfo2 import get_user_info as get_user_info2
from .get_courses import get_courses
from .downfile import down_file
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

if 'proxy' in get_driver().config:
    proxy = get_driver().config.proxy
else:
    proxy = None
if proxy:
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }
else:
    proxies = None


async def handle_sw_command(matcher: Matcher, db_conn, qid, ater, args):
    if ater:
        if len(args) == 0:
            key = None
        elif len(args) == 1:
            key = args[0]
        else:
            return await matcher.send('请输入正确的指令', at_sender=True)
        sw = get_sw(db_conn, ater, key)
        if sw:
            await matcher.send('你查询的用户sw为{0}'.format(sw), at_sender=True)
        else:
            await matcher.send('你查询的用户sw尚未绑定', at_sender=True)
    else:
        if len(args) == 0:
            sw = get_sw(db_conn, qid)
            if sw:
                await matcher.send('你的sw为{0}'.format(sw), at_sender=True)
            else:
                await matcher.send('你的sw尚未绑定', at_sender=True)
        elif len(args) == 1 and args[0] == 'unbind':
            unset_sw(db_conn, qid)
            await matcher.send('你的sw信息已解绑', at_sender=True)
        elif len(args) == 1 and args[0] != 'unbind':
            sw = get_sw(db_conn, qid, args[0])
            if sw:
                await matcher.send('你的sw为{0}'.format(sw), at_sender=True)
            else:
                await matcher.send('你的sw尚未绑定', at_sender=True)
        elif len(args) == 2 and args[0] == 'unbind':
            key = args[1]
            unset_sw(db_conn, qid, key)
            await matcher.send('你的sw信息已解绑', at_sender=True)
        elif len(args) == 2 and args[0] == 'bind':
            sw = args[1]
            set_sw(db_conn, qid, sw)
            await matcher.send('你的sw已绑定为{0}'.format(sw), at_sender=True)
        elif len(args) == 3 and args[0] == 'bind':
            sw = args[1]
            key = args[2]
            set_sw(db_conn, qid, sw, key)
            await matcher.send('你的sw已绑定为{0}'.format(sw), at_sender=True)


async def handle_id_command(matcher: Matcher, db_conn, qid, ater, args):
    if ater:
        if len(args) == 0:
            key = None
        elif len(args) == 1:
            key = args[0]
        else:
            return await matcher.send('请输入正确的指令', at_sender=True)
        mid = get_id(db_conn, ater, key)
        if mid:
            await matcher.send('你查询的用户id为{0}'.format(mid), at_sender=True)
        else:
            await matcher.send('你查询的用户id尚未绑定', at_sender=True)
    else:
        if len(args) == 0:
            mid = get_id(db_conn, qid)
            if mid:
                await matcher.send('你的id为{0}'.format(mid), at_sender=True)
            else:
                await matcher.send('你的id尚未绑定', at_sender=True)
        elif len(args) == 1 and args[0] == 'unbind':
            unset_id(db_conn, qid)
            await matcher.send('你的id信息已解绑', at_sender=True)
        elif len(args) == 1 and args[0] != 'unbind':
            mid = get_id(db_conn, qid, args[0])
            if mid:
                await matcher.send('你的id为{0}'.format(mid), at_sender=True)
            else:
                await matcher.send('你的id尚未绑定', at_sender=True)
        elif len(args) == 2 and args[0] == 'unbind':
            key = args[1]
            unset_id(db_conn, qid, key)
            await matcher.send('你的id信息已解绑', at_sender=True)
        elif len(args) == 2 and args[0] == 'bind':
            mid = args[1]
            set_id(db_conn, qid, mid)
            await matcher.send('你的id已绑定为{0}'.format(mid), at_sender=True)
        elif len(args) == 3 and args[0] == 'bind':
            mid = args[1]
            key = args[2]
            set_id(db_conn, qid, mid, key)
            await matcher.send('你的id已绑定为{0}'.format(mid), at_sender=True)


async def handle_bind_command(matcher: Matcher, db_conn, qid, ater, args):
    if ater:
        qid = ater
    bind = get_bind(db_conn, qid)
    if not bind:
        await matcher.send('尚未绑定任何信息', at_sender=True)
    else:
        await matcher.send(bind, at_sender=True)


async def handle_default_command(matcher: Matcher, db_conn, qid, ater, args):
    if len(args) != 1:
        return await matcher.send('指令无效', at_sender=True)
    default = args[0]
    r = set_default(db_conn, qid, default)
    if not r:
        await matcher.send('尚未绑定{0}信息'.format(default), at_sender=True)
    else:
        await matcher.send('默认查询设置成功', at_sender=True)


async def handle_card_command(bot: Bot, matcher: Matcher, db_conn, gid, qid, sender_nickname, ater, args):
    if len(args) == 0:
        role = get_role()
        key = None
    elif len(args) == 1:
        role = get_role()
        key = args[0]
    elif len(args) == 2:
        role = get_role(args[0])
        key = args[1]
    if not role:
        return
    if ater:
        ater_info = await bot.get_group_member_info(group_id=gid, user_id=int(ater))
        nickname = ater_info['nickname']
        avatar = 'http://q1.qlogo.cn/g?b=qq&nk={0}&s=640'.format(ater)
        sw = get_sw(db_conn, ater, key)
        mid = get_id(db_conn, ater, key)
        card_user = ater
    else:
        nickname = sender_nickname
        avatar = 'http://q1.qlogo.cn/g?b=qq&nk={0}&s=640'.format(qid)
        sw = get_sw(db_conn, qid, key)
        mid = get_id(db_conn, qid, key)
        card_user = qid
    if not sw and not mid:
        return await matcher.send('尚未绑定任何信息', at_sender=True)
    if not sw:
        sw = '未绑定'
    if not mid:
        mid = '未绑定'
    get_card(avatar, role, nickname, card_user, sw, mid)
    await matcher.send(
        MessageSegment.image(pic_data('pic/card/{0}-card.png'.format(card_user))),
        at_sender=True)


async def handle_info_command(bot, matcher: Matcher, db_conn, qid, ater, args, show_type):
    if len(args) > 1:
        await matcher.send('请输入正确的查询命令', at_sender=True)
        return
    if len(args) == 0:
        if ater:
            mid = get_id(db_conn, ater)
        else:
            mid = get_id(db_conn, qid)
        if not mid:
            await matcher.send('用户id尚未绑定', at_sender=True)
            return
    elif len(args) == 1:
        key = args[0]
        if ater:
            qid = ater
        mid = get_id(db_conn, qid, key)
        if not mid:
            mid = args[0]
        if len(mid) != 9 and len(mid) != 11:
            await matcher.send('不正确的工匠id', at_sender=True)
            return
    if show_type == 1:
        error = get_user_info(mid, proxies)
    else:
        error = get_user_info2(mid, proxies)
    if not error:
        await matcher.send(
            MessageSegment.image(pic_data('pic/info/{0}.png'.format(mid))),
            at_sender=True)
    else:
        await matcher.send(error, at_sender=True)


async def handle_detail_command(bot, matcher: Matcher, db_conn, qid, ater, args):
    if not (len(args) <= 2 and (len(args[0]) == 9 or len(args[0]) == 11)):
        await matcher.send('请输入正确的关卡id', at_sender=True)
        return
    courseid = args[0]
    filter_type = ''
    if len(args) == 2:
        filter_type = args[1]
    error = get_course_detail(courseid, filter_type, proxies)
    if not error:
        await matcher.send(
            MessageSegment.image(pic_data('pic/detail/{0}.png'.format(courseid))),
            at_sender=True)
    else:
        await matcher.send(error, at_sender=True)


async def handle_course_command(bot, matcher: Matcher, db_conn, qid, ater, args, ctype):
    is_showmii = False
    is_showthumbnail = False
    if 'mii' in args or ctype == 'record':
        is_showmii = True
    if 'thumbnail' in args:
        is_showthumbnail = True
    if ater:
        mid = get_id(db_conn, ater)
    else:
        mid = get_id(db_conn, qid)
    if len(args) == 1:
        key = args[0]
        if ater:
            qid = ater
        mid = get_id(db_conn, qid, key)
        if not mid:
            mid = args[0]
        if len(mid) != 9 and len(mid) != 11:
            await matcher.send('不合法的工匠id', at_sender=True)
            return
    if not mid:
        await matcher.send('用户id尚未绑定', at_sender=True)
    else:
        error = get_courses(mid, ctype, is_showmii, is_showthumbnail, proxies)
        if not error:
            await matcher.send(
                MessageSegment.image(pic_data('pic/courses/{0}-{1}.png'.format(mid, ctype))),
                at_sender=True)
        else:
            await matcher.send(error, at_sender=True)


async def handle_view_command(bot, matcher: Matcher, db_conn, qid, ater, args):
    if not (len(args) == 1 and (len(args[0]) == 9 or len(args[0]) == 11)):
        await matcher.send('请输入正确的关卡id', at_sender=True)
        return
    courseid = args[0]
    url = 'https://tgrcode.com/mm2/level_data/' + courseid
    code, error = down_file(url, 'pic/map/' + courseid, proxies)
    if code != 200:
        await matcher.send(error, at_sender=True)
        return
    out = subprocess.getoutput('toost -p pic/map/{0} -a 2 -o pic/map/{0}-o.png -s pic/map/{0}-s.png'.format(courseid))
    for line in out.split('\n'):
        if 'Done parsing ' in line:
            course_name = line.split('Done parsing ')[1]
    message = MessageSegment.text('图片生成失败')
    if os.path.exists('pic/map/{0}-o.png'.format(courseid)):
        #message = MessageSegment.text('\n{0}\n表世界'.format(course_name)) + MessageSegment.image(
        message = MessageSegment.image(
            pic_data('pic/map/{0}-o.png'.format(courseid)))
    if os.path.exists('pic/map/{0}-s.png'.format(courseid)):
        img = Image.open('pic/map/{0}-s.png'.format(courseid))
        w, h = img.size
        img = img.crop((0, 0, w, h - 20))
        img.save('pic/map/{0}-crop.png'.format(courseid))
        if not \
                subprocess.getoutput(
                    'md5sum pic/map/{0}-crop.png'.format(courseid)).split(
                    ' ')[0] == 'f5db35c5867183e6af8db333cfcdc257':
            #message += MessageSegment.text('里世界') + MessageSegment.image(pic_data('pic/map/{0}-s.png'.format(courseid)))
            message += MessageSegment.image(pic_data('pic/map/{0}-s.png'.format(courseid)))
        #else:
            #message += MessageSegment.text('里世界为空')
    await matcher.send(message, at_sender=True)
