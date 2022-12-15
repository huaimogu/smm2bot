import requests
from PIL import Image, ImageDraw, ImageFont
from .downfile import down_file
from .utils import draw_text_center_withlines
from .utils import draw_text_right
from .utils import transid


def get_user_info(mid, proxies):
    url = 'https://tgrcode.com/mm2/user_info/{0}'.format(mid)
    try:
        rq = requests.get('{0}/{1}'.format(url, mid), proxies=proxies)
        i = 0
        while i < 1 and (rq.status_code != 200 or rq.text == ''):
            rq = requests.get(url, proxies=proxies)
            i = i + 1
        if rq.status_code != 200:
            return rq.text
        response = rq.json()
        im_bg = Image.open('pic/info2.png')
        down_file(response['mii_image'], 'pic/info/{0}-mii.png'.format(mid), proxies)
        im_avatar = Image.open('pic/info/{0}-mii.png'.format(mid)).resize((126, 126), Image.ANTIALIAS)
        r, g, b, a = im_avatar.split()
        im_bg.paste(im_avatar, (218, 100, 344, 226), mask=a)
        font = ImageFont.truetype('pic/yaheibold.ttf', size=16)
        font2 = ImageFont.truetype('pic/yaheibold.ttf', size=18)
        font3 = ImageFont.truetype('pic/yaheibold.ttf', size=25)
        font4 = ImageFont.truetype('pic/yaheibold.ttf', size=15)
        font_color = (75, 19, 22)
        font_color2 = (126, 110, 107)
        draw = ImageDraw.Draw(im_bg)
        draw_text_center_withlines(draw, (34, 266), (530, 314), '马力欧耐力挑战', font, font_color)
        draw_text_center_withlines(draw, (552, 266), (962, 314), '关卡的游玩信息', font, font_color)
        draw_text_center_withlines(draw, (554, 32), (964, 73), '多人对战', font, font_color)
        draw_text_center_withlines(draw, (554, 147), (964, 192), '多人过关', font, font_color)
        draw.text(xy=(45, 325), text=str('"简单"的最高纪录'), fill=font_color, font=font)
        draw.text(xy=(45, 364), text=str('"普通"的最高纪录'), fill=font_color, font=font)
        draw.text(xy=(45, 403), text=str('"困难"的最高纪录'), fill=font_color, font=font)
        draw.text(xy=(45, 440), text=str('"极难"的最高纪录'), fill=font_color, font=font)
        draw_text_right(draw, (515, 323), str(response['easy_highscore']), font2, font_color)
        draw_text_right(draw, (515, 362), str(response['normal_highscore']), font2, font_color)
        draw_text_right(draw, (515, 401), str(response['expert_highscore']), font2, font_color)
        draw_text_right(draw, (515, 438), str(response['super_expert_highscore']), font2, font_color)
        draw.text(xy=(564, 325), text=str('游玩的关卡数'), fill=font_color, font=font)
        draw.text(xy=(564, 364), text=str('过关的关卡数'), fill=font_color, font=font)
        draw.text(xy=(564, 403), text=str('挑战的马力欧数'), fill=font_color, font=font)
        draw.text(xy=(564, 440), text=str('失败的马力欧数'), fill=font_color, font=font)
        draw_text_right(draw, (952, 323), str(response['courses_played']), font2, font_color)
        draw_text_right(draw, (952, 362), str(response['courses_cleared']), font2, font_color)
        draw_text_right(draw, (952, 401), str(response['courses_attempted']), font2, font_color)
        draw_text_right(draw, (952, 438), str(response['courses_deaths']), font2, font_color)
        draw.text(xy=(564, 80), text=str('获胜数'), fill=font_color, font=font)
        draw.text(xy=(564, 117), text=str('游玩数'), fill=font_color, font=font)
        draw.text(xy=(564, 200), text=str('过关数'), fill=font_color, font=font)
        draw.text(xy=(564, 237), text=str('游玩数'), fill=font_color, font=font)
        draw_text_right(draw, (952, 78), str(response['versus_won']), font2, font_color)
        draw_text_right(draw, (952, 115), str(response['versus_plays']), font2, font_color)
        draw_text_right(draw, (952, 198), str(response['coop_clears']), font2, font_color)
        draw_text_right(draw, (952, 235), str(response['coop_plays']), font2, font_color)
        draw.text(xy=(72, 38), text=str(response['likes']), fill=font_color, font=font3)
        if response['versus_rating'] < 6000:
            rank_color = font_color
        else:
            rank_color = (255, 106, 106)
        if response['versus_rating'] < 5000:
            rank_color = font_color
            draw.text(xy=(506, 30), text=str(response['versus_rank_name']), fill=rank_color, font=font3)
        else:
            draw.text(xy=(506, 30), text='S', fill=rank_color, font=font3)
            draw.text(xy=(520, 36), text=str('+'), fill=rank_color, font=font4)
        draw.text(xy=(465, 40), text=str(response['versus_rating']), fill=rank_color, font=font4)
        draw.rectangle(((460, 62), (528, 65)), fill=(20, 20, 20))
        draw.rectangle(((460, 62), (460 + (528-460) * (response['versus_rating'] % 1000) / 1000, 65)), fill=(255, 189, 2))
        draw.text(xy=(45, 220), text=str('ID: {0}'.format(transid(response['code']))), fill=font_color2, font=font)
        draw.text(xy=(45, 240), text=str('NAME: {0}'.format(response['name'])), fill=font_color2, font=font)
        im_bg.save('pic/info/{0}.png'.format(mid))
        return None
    except Exception as e:
        return str(e)


