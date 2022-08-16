from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent, Bot,
)
from nonebot import get_driver
from nonebot.params import CommandArg
from .utils import get_conn
from .utils import get_message_ater
from .utils import get_command_args
from .utils import cant_query
from .utils import block_user
from .utils import unblock_user
from .utils import white_user
from .utils import unwhite_user
from .utils import is_block_user
from .router import handle_sw_command
from .router import handle_id_command
from .router import handle_bind_command
from .router import handle_default_command
from .router import handle_card_command
from .router import handle_info_command
from .router import handle_detail_command
from .router import handle_view_command
from .router import handle_course_command


smmdb = get_conn()
sw_matcher = on_command("sw")
id_matcher = on_command("id")
card_matcher = on_command('card')
info_matcher = on_command('info')
info2_matcher = on_command('info2')
detail_matcher = on_command('detail')
post_matcher = on_command('post')
play_matcher = on_command('play')
like_matcher = on_command('like')
first_matcher = on_command('first')
record_matcher = on_command('record')
view_matcher = on_command('view')
bind_matcher = on_command('bind')
default_matcher = on_command('default')
block_marher = on_command('大师', permission=SUPERUSER)
unblock_marher = on_command('不是大师', permission=SUPERUSER)
white_marher = on_command('笨比', permission=SUPERUSER)
unwhite_marher = on_command('不是笨比', permission=SUPERUSER)
help_matcher = on_command('help')


@block_marher.handle()
async def _(event: MessageEvent):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    block_user(smmdb, ater)
    await block_marher.send('大师好!')


@unblock_marher.handle()
async def _(event: MessageEvent):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    unblock_user(smmdb, ater)
    await unblock_marher.send('发生什么事了?')


@white_marher.handle()
async def _(event: MessageEvent):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    white_user(smmdb, ater)
    await block_marher.send('笨比好!')


@unwhite_marher.handle()
async def _(event: MessageEvent):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    unwhite_user(smmdb, ater)
    await unblock_marher.send('发生什么事了?')


@sw_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    await handle_sw_command(sw_matcher, smmdb, qid, ater, args)


@id_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    await handle_id_command(sw_matcher, smmdb, qid, ater, args)


@bind_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    await handle_bind_command(bind_matcher, smmdb, qid, ater, args)


@default_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    await handle_default_command(default_matcher, smmdb, qid, ater, args)


@card_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    sender_nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    await handle_card_command(bot, card_matcher, smmdb, gid, qid, sender_nickname, ater, args)


@info_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_info_command(bot, info_matcher, smmdb, qid, ater, args, 1)


@info2_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_info_command(bot, info2_matcher, smmdb, qid, ater, args, 2)


@detail_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_detail_command(bot, detail_matcher, smmdb, qid, ater, args)


@post_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_course_command(bot, post_matcher, smmdb, qid, ater, args, 'post')


@play_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_course_command(bot, play_matcher, smmdb, qid, ater, args, 'play')


@like_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_course_command(bot, like_matcher, smmdb, qid, ater, args, 'like')


@first_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_course_command(bot, first_matcher, smmdb, qid, ater, args, 'first')


@record_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_course_command(bot, record_matcher, smmdb, qid, ater, args, 'record')


@view_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = get_message_ater(event.raw_message)
    args = get_command_args(foo.extract_plain_text())
    if event.message_type == 'group':
        gid = event.group_id
    else:
        gid = 0
    nickname = event.sender.card if event.sender.card != '' else event.sender.nickname
    err = cant_query(smmdb, qid, nickname)
    if err:
        await info_matcher.send(err)
        return
    await handle_view_command(bot, view_matcher, smmdb, qid, ater, args)


@help_matcher.handle()
async def _():
    await help_matcher.send('【金山文档】 bot帮助文档https://kdocs.cn/l/saSleN4dPYUj', at_sender=True)

