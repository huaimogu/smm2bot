import requests
from PIL import Image, ImageDraw, ImageFont
from .utils import draw_text_center_withlines
from .utils import transid
from .downfile import down_file


def get_user_info(mid, proxies):
    url = 'https://tgrcode.com/mm2/user_info/{0}'.format(mid)
    try:
        r = requests.get(url, proxies=proxies, timeout=500)
        if r.status_code != 200:
            return r.json()['error']
        response = r.json()
        im_bg = Image.open('pic/info.png')
        down_file(response['mii_image'], 'pic/info/{0}-mii.png'.format(mid), proxies)
        im_avatar = Image.open('pic/info/{0}-mii.png'.format(mid)).resize((400, 400), Image.ANTIALIAS)
        r, g, b, a = im_avatar.split()
        im_bg.paste(im_avatar, (20, 10, 420, 410), mask=a)
        font = ImageFont.truetype('pic/yaheibold.ttf', size=32)
        font_color = (0, 0, 0)
        draw = ImageDraw.Draw(im_bg)

        draw.text(xy=(680, 110), text=str(response['courses_played']), fill=font_color, font=font)
        draw.text(xy=(680, 157), text=str(response['courses_cleared']), fill=font_color, font=font)
        draw.text(xy=(680, 204), text=str(response['courses_attempted']), fill=font_color, font=font)
        draw.text(xy=(680, 251), text=str(response['courses_deaths']), fill=font_color, font=font)
        draw.text(xy=(680, 298), text=str(response['first_clears']), fill=font_color, font=font)
        draw.text(xy=(680, 345), text=str(response['world_records']), fill=font_color, font=font)

        draw.text(xy=(600, 550), text=str(response['easy_highscore']), fill=font_color, font=font)
        draw.text(xy=(600, 597), text=str(response['normal_highscore']), fill=font_color, font=font)
        draw.text(xy=(600, 644), text=str(response['expert_highscore']), fill=font_color, font=font)
        draw.text(xy=(600, 691), text=str(response['super_expert_highscore']), fill=font_color, font=font)

        draw.text(xy=(1115, 785), text=str(response['coop_plays']), fill=font_color, font=font)
        draw.text(xy=(1115, 832), text=str(response['coop_clears']), fill=font_color, font=font)
        draw.text(xy=(220, 795), text=str(response['maker_points']), fill=font_color, font=font)
        draw.text(xy=(220, 855), text=str(response['uploaded_levels']), fill=font_color, font=font)
        draw.text(xy=(560, 795), text=str(response['likes']), fill=font_color, font=font)
        last_active_time = response['last_active_pretty'].split(' ')[0].split('-')
        draw.text(xy=(560, 855), text='{0}-{1}-{2}'.format(last_active_time[2], last_active_time[1],last_active_time[0]), fill=font_color, font=font)

        draw.text(xy=(1100, 113), text=str(response['versus_rank_name']), fill=font_color, font=font)
        draw.text(xy=(1100, 160), text=str(response['versus_rating']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 1), text=str(response['versus_plays']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 2), text=str(response['versus_won']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 3), text='0' if response['versus_plays'] == 0 else '{:.2%}'.format(response['versus_won'] / response['versus_plays']),
                  fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 4), text=str(response['versus_kills']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 5), text=str(response['versus_killed_by_others']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 6), text=str(response['versus_win_streak']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 7), text=str(response['versus_lose_streak']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 8), text=str(response['recent_performance']), fill=font_color, font=font)
        draw.text(xy=(1100, 160 + 47 * 9), text=str(response['versus_disconnected']), fill=font_color, font=font)
        draw_text_center_withlines(draw, (20, 505), (412, 535), response['name'], font, font_color)
        draw_text_center_withlines(draw, (20, 580), (412, 615), transid(response['code']), font, font_color)
        im_bg.save('pic/info/{0}.png'.format(mid))
        return None
    except Exception as e:
        return str(e)


