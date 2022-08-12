import time
import math
import json
import random
from redis import ConnectionPool, Redis


def get_conn():
    pool = ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)
    return Redis(connection_pool=pool)


def block_user(conn, uid):
    conn.hset(uid, 'block', 'yes')


def unblock_user(conn, uid):
    conn.hset(uid, 'block', 'no')


def is_block_user(conn, uid):
    v = conn.hget(uid, 'block')
    if v == 'yes':
        return True
    else:
        return False


def white_user(conn, uid):
    conn.hset(uid, 'white', 'yes')


def unwhite_user(conn, uid):
    conn.hset(uid, 'white', 'no')


def is_white_user(conn, uid):
    v = conn.hget(uid, 'white')
    if v == 'yes':
        return True
    else:
        return False


def set_default(conn, qid, default):
    conn.hset(qid, 'default', default)
    return True


def set_sw(conn, qid, sw, key=None):
    if not key:
        key = conn.hget(qid, 'default')
        if key == '' or not key:
            key = conn.hset(qid, 'default', '1')
            key = '1'
    info_str = conn.hget(qid, 'info')
    if not info_str:
        info = {key: {'sw': sw}}
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            info[key] = {'sw': sw}
        else:
            info[key]['sw'] = sw
    conn.hset(qid, 'info', json.dumps(info))


def unset_sw(conn, qid, key=None):
    if not key:
        key = conn.hget(qid, 'default')
    info_str = conn.hget(qid, 'info')
    if not info_str:
        return
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            return
        else:
            if 'id' in info[key].keys() and info[key]['id'] != '':
                info[key]['sw'] = ''
                conn.hset(qid, 'info', json.dumps(info))
            else:
                info.pop(key)
                conn.hset(qid, 'info', json.dumps(info))


def get_sw(conn, qid, key=None):
    if not key:
        key = conn.hget(qid, 'default')
        if key == '':
            key = conn.hset(qid, 'default', '1')
            key = '1'
    info_str = conn.hget(qid, 'info')
    if not info_str:
        return None
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            return None
        else:
            if 'sw' in info[key].keys():
                sw = info[key]['sw']
                return sw


def set_id(conn, qid, uid, key=None):
    if not key:
        key = conn.hget(qid, 'default')
        if key == '' or not key:
            key = conn.hset(qid, 'default', '1')
            key = '1'
    info_str = conn.hget(qid, 'info')
    if not info_str:
        info = {key: {'id': uid}}
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            info[key] = {'id': uid}
        else:
            info[key]['id'] = uid
    conn.hset(qid, 'info', json.dumps(info))


def unset_id(conn, qid, key=None):
    if not key:
        key = conn.hget(qid, 'default')
    info_str = conn.hget(qid, 'info')
    if not info_str:
        return
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            return
        else:
            if 'sw' in info[key].keys() and info[key]['sw'] != '':
                info[key]['id'] = ''
                conn.hset(qid, 'info', json.dumps(info))
            else:
                info.pop(key)
                conn.hset(qid, 'info', json.dumps(info))


def get_id(conn, qid, key=None):
    if not key:
        key = conn.hget(qid, 'default')
    info_str = conn.hget(qid, 'info')
    if not info_str:
        return None
    else:
        info = json.loads(info_str)
        if key not in info.keys():
            return None
        else:
            if 'id' in info[key].keys():
                uid = info[key]['id']
                return uid


def get_bind(conn, qid):
    result = ''
    default = conn.hget(qid, 'default')
    info_str = conn.hget(qid, 'info')
    if not info_str:
        return None
    else:
        info = json.loads(info_str)
        result += '\ndefault：{0}'.format(default)
        for k, v in info.items():
            result += '\n' + k
            for k2, v2 in v.items():
                if k2 == 'id':
                    result += '\nid: {0}'.format(v2)
                else:
                    result += '\nsw: {0}'.format(v2)
        return result


def transcode(mid):
    if mid is None:
        return ""
    mid = mid.upper()
    if len(mid) == 11:
        mid = mid.split('-')[0] + mid.split('-')[1] + mid.split('-')[2]
    return mid


def cant_query(conn, qid, nickname):
    ts = int(time.time())
    interval = 5
    last_query = conn.get('last_query')
    if not last_query:
        conn.set('last_query', ts)
    last_query = int(last_query)
    if (ts - last_query) > interval:
        conn.set('last_query', ts)
    else:
        return '蘑菇需要休息休息，请{0}秒后再来查询'.format(interval - ts + last_query)
    if is_block_user(conn, qid):
        return '{0}是大师!'.format(nickname)
    if is_white_user(conn, qid):
        return False
    mid = transcode(get_id(conn, qid))
    if len(mid) != 9:
        return '先绑定工匠id后再来查询吧'
    return False


def get_command_args(text):
    args = text.strip().split(' ')
    if len(args) == 1 and args[0] == '':
        args = []
    return args


def get_message_ater(cq):
    ater = None
    if 'CQ:at' in cq:
        ater = cq.split('qq=')[1].split(']')[0]
    return ater


def get_role(role=None):
    if not role:
        num = random.randint(1, 4)
        if num == 1:
            return 'mario'
        elif num == 2:
            return 'luigi'
        elif num == 3:
            return 'kinopio'
        elif num == 4:
            return 'kinopiko'
        else:
            return None
    else:
        if role == 'M':
            return 'mario'
        elif role == 'L':
            return 'luigi'
        elif role == 'O':
            return 'kinopio'
        elif role == 'K':
            return 'kinopiko'
        else:
            return None


def draw_text_center_withlines(draw, xy1, xy2, words, font, font_color, hsplit=2):
    if len(words) == 0:
        return
    w = xy2[0] - xy1[0]
    h = xy2[1] - xy1[1]
    font_w, font_h = font.getsize(words)
    lines = math.ceil(font_w / w)
    split_len = math.ceil(len(words) / math.ceil(font_w / w))
    texts = [words[i:i + split_len] for i in range(0, len(words), split_len)]
    h_start = xy1[1] + (h - (lines - 1) * hsplit - lines * font_h) / 2
    index = 0
    for text in texts:
        w1, h1 = font.getsize(text)
        draw.text(xy=(xy1[0] + (w - w1) / 2, h_start), text=text, fill=font_color, font=font)
        h_start += font_h + hsplit
        index += 1


def draw_text_right(draw, xy1, words, font, font_color):
    font_w, font_h = font.getsize(words)
    draw.text(xy=(xy1[0] - font_w, xy1[1]), text=words, fill=font_color, font=font)


def transid(id):
    return '{0}-{1}-{2}'.format(id[0:3], id[3:6], id[6:9])


def pic_data(file_name):
    with open(file_name, 'rb') as obj:
        return obj.read()
