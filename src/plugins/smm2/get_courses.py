import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from .downfile import down_file
from .utils import draw_text_center_withlines
from .utils import draw_text_right
from .utils import transid


def get_courses(mid, ctype, is_showmii, is_showthumbnail, proxies):
    if ctype == 'post' or ctype == 'postall':
        url = 'https://tgrcode.com/mm2/get_posted'
    elif ctype == 'play':
        url = 'https://tgrcode.com/mm2/get_played'
    elif ctype == 'like':
        url = 'https://tgrcode.com/mm2/get_liked'
    elif ctype == 'first':
        url = 'https://tgrcode.com/mm2/get_first_cleared'
    elif ctype == 'record':
        url = 'https://tgrcode.com/mm2/get_world_record'
    try:
        rq = requests.get('{0}/{1}'.format(url, mid), proxies=proxies)
        i = 0
        while i < 1 and (rq.status_code != 200 or rq.text == ''):
            rq = requests.get(url, proxies=proxies)
            i = i + 1
        if rq.status_code != 200:
            return rq.text
        response = rq.json()
        courses = response['courses']
        if len(courses) > 10 and ctype == 'post':
            courses = courses[:10]
        if len(courses) == 0:
            return '无符合条件的关卡信息'
        h = 420
        w = 1000
        img = Image.new('RGB', (w, h * len(courses) + 20), (255, 255, 255))
        font = ImageFont.truetype('pic/yaheibold.ttf', size=32)
        font2 = ImageFont.truetype('pic/yaheibold.ttf', size=21)
        font3 = ImageFont.truetype('pic/yaheibold.ttf', size=28)
        font_color = (66, 5, 12)
        draw = ImageDraw.Draw(img)
        for index, course in enumerate(courses):
            card_img = Image.open('pic/coursebg.png')
            if not is_showthumbnail:
                smm_type = course['game_style_name']
                smm_type_img = Image.open('pic/{0}.png'.format(smm_type))
            else:
                if not os.path.exists('pic/courses/{0}-thumbnail.png'.format(course['course_id'])):
                    down_file('https://tgrcode.com/mm2/level_thumbnail/{0}'.format(course['course_id']), 'pic/courses/{0}-thumbnail.png'.format(course['course_id']), proxies)
                smm_type_img = Image.open('pic/courses/{0}-thumbnail.png'.format(course['course_id'])).resize((240, 128), Image.LANCZOS)
            img.paste(card_img, (0, index * h, w, (index + 1) * 420))
            img.paste(smm_type_img, (20, index * h + 40, 260, index * h + 168))
            draw.text(xy=(280, index * h + 40), text=str(course['name']), fill=font_color, font=font3)
            draw.text(xy=(330, index * h + 92), text=str(course['likes']), fill=font_color, font=font)
            draw.text(xy=(555, index * h + 92), text=str(course['boos']), fill=font_color, font=font)
            draw.text(xy=(320, index * h + 139), text=str(course['tags_name'][0]), fill=font_color, font=font2)
            draw.text(xy=(552, index * h + 139), text=str(course['tags_name'][1]), fill=font_color, font=font2)
            uptime = time.strftime("%Y/%m/%d %H:%M ", time.localtime(course['uploaded']))
            draw_text_right(draw, (980, index * h + 110), 'uptime:{0}'.format(uptime), font2,
                            font_color)
            draw_text_right(draw, (980, index * h + 85), 'uploader:{0}'.format(course['uploader']['name']), font2,
                            font_color)
            difficulty = course['difficulty']
            if difficulty == 0:
                difficulty_name = '简单'
            if difficulty == 1:
                difficulty_name = '普通'
            if difficulty == 2:
                difficulty_name = '困难'
            if difficulty == 3:
                difficulty_name = '极难'
            draw_text_right(draw, (960, index * h + 139), '难度:{0}'.format(difficulty_name), font2, font_color)
            draw_text_center_withlines(draw, (23, index * h + 182), (974, index * h + 288), course['description'],
                                       font2, font_color)
            draw.text(xy=(130, index * h + 310), text='最短时间', fill=font_color, font=font2)
            draw.text(xy=(465, index * h + 310), text='通过率', fill=font_color, font=font2)
            draw.text(xy=(800, index * h + 310), text='关卡ID', fill=font_color, font=font2)
            draw.text(xy=(160, index * h + 340),
                      text=course['world_record_pretty'] if 'world_record_pretty' in course.keys() else '--',
                      fill=font_color, font=font2)
            draw.text(xy=(130, index * h + 370),
                      text=course['record_holder']['name'] if 'record_holder' in course.keys() else '--',
                      fill=font_color,
                      font=font2)
            a,b,c,d = font.getbbox('{0}/{1}'.format(course['clears'], course['attempts']))
            w3 = c - a
            h3 = d - b
            draw.text(xy=(354 + (292 - w3) / 2, index * h + 350),
                      text='{0}/{1}'.format(course['clears'], course['attempts']), fill=font_color, font=font)
            a,b,c,d = font.getbbox(transid(course['course_id']))
            w4 = c - a
            h4 = d - b
            draw.text(xy=(684+(292-w4)/2, index * h + 350), text=transid(course['course_id']), fill=font_color, font=font)
            if is_showmii and 'record_holder' in course.keys():
                if not os.path.exists('pic/info/{0}-mii.png'.format(course['record_holder']['code'])):
                    try:
                        down_file(course['record_holder']['mii_image'],
                                  'pic/info/{0}-mii.png'.format(course['record_holder']['code']), proxies)
                    except Exception as e:
                        return 'mii下载失败，请重试'
                im_avatar = Image.open('pic/info/{0}-mii.png'.format(course['record_holder']['code'])).resize((70, 70),
                                                                                                              Image.LANCZOS)
                r, g, b, a = im_avatar.split()
                img.paste(im_avatar, (40, index * h + 315, 110, index * h + 385), mask=a)
        if len(courses) > 20:
            rate = 15 / len(courses)
            img = img.resize((int(w * rate), int((h * len(courses) + 20) * rate)))
        img.save('pic/courses/{0}-{1}.png'.format(mid, ctype))
        return None
    except Exception as e:
        return str(e)
