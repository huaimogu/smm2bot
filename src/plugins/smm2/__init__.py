from nonebot import on_command
from nonebot.adapters.qq import (
    Message,
    MessageSegment,
    MessageEvent, Bot,
)
from nonebot.params import CommandArg
from .utils import get_conn
from .utils import get_message_ater
from .utils import get_command_args
from .utils import block_user
from .utils import unblock_user
from .utils import white_user
from .utils import unwhite_user
from .utils import is_block_user
from .utils import pic_data
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
postall_matcher = on_command('postall')
play_matcher = on_command('play')
like_matcher = on_command('like')
first_matcher = on_command('first')
record_matcher = on_command('record')
view_matcher = on_command('view')
bind_matcher = on_command('bind')
default_matcher = on_command('default')
help_matcher = on_command('help')


@sw_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_sw_command(sw_matcher, smmdb, qid, ater, args)


@id_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_id_command(sw_matcher, smmdb, qid, ater, args)


@bind_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_bind_command(bind_matcher, smmdb, qid, ater, args)


@default_matcher.handle()
async def _(event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_default_command(default_matcher, smmdb, qid, ater, args)


@card_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    gid = 0
    ater = None
    args = get_command_args(foo.extract_plain_text())
    sender_nickname = ''
    await handle_card_command(bot, card_matcher, smmdb, gid, qid, sender_nickname, ater, args)


@info_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_info_command(bot, info_matcher, smmdb, qid, ater, args, 1)


@info2_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_info_command(bot, info2_matcher, smmdb, qid, ater, args, 2)


@detail_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_detail_command(bot, detail_matcher, smmdb, qid, ater, args)


@post_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, post_matcher, smmdb, qid, ater, args, 'post')


@postall_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, post_matcher, smmdb, qid, ater, args, 'postall')


@play_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, play_matcher, smmdb, qid, ater, args, 'play')


@like_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, like_matcher, smmdb, qid, ater, args, 'like')


@first_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, first_matcher, smmdb, qid, ater, args, 'first')


@record_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_course_command(bot, record_matcher, smmdb, qid, ater, args, 'record')


@view_matcher.handle()
async def _(bot: Bot, event: MessageEvent, foo: Message = CommandArg()):
    qid = event.get_user_id()
    ater = None
    args = get_command_args(foo.extract_plain_text())
    await handle_view_command(bot, view_matcher, smmdb, qid, ater, args)


@help_matcher.handle()
async def _():
    await help_matcher.send(MessageSegment.file_image(data=pic_data('pic/help.png')), at_sender=True)

