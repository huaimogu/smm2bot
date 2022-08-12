import requests
from PIL import Image, ImageDraw, ImageFont
from .downfile import down_file
from .utils import draw_text_center_withlines


def get_course_detail(cid, filter_type, proxies):
    url1 = 'https://tgrcode.com/mm2/level_info/{0}'.format(cid)
    url2 = 'https://tgrcode.com/mm2/level_played/{0}'.format(cid)
    try:
        r1 = requests.get(url1, proxies=proxies, timeout=500)
        if r1.status_code != 200:
            return r1.json()['error']
        response1 = r1.json()
        r2 = requests.get(url2, proxies=proxies, timeout=500)
        if r2.status_code != 200:
            return r2.json()['error']
        response2 = r2.json()
        h = 112
        w = 581
        players = []
        for player in response2['players']:
            if filter_type == 'clear':
                if player['pid'] in response2['cleared']:
                    players.append(player)
            elif filter_type == 'like':
                if player['pid'] in response2['liked']:
                    players.append(player)
            else:
                players.append(player)
        if len(players) >= 100:
            players = players[0:100]
        if len(players) < 7:
            total_h = 1047
        else:
            total_h = 320 + 112 * len(players) + 15
        img = Image.new('RGB', (1793, total_h), (255, 255, 255))
        bg_img = Image.open('pic/detail-bg.png')
        img.paste(bg_img, (0, 0, 1793, 1047))
        font = ImageFont.truetype('pic/yaheibold.ttf', size=25)
        font2 = ImageFont.truetype('pic/yaheibold.ttf', size=40)
        font_color = (75, 19, 22)
        draw = ImageDraw.Draw(img)
        down_file('https://tgrcode.com/mm2/level_thumbnail/{0}'.format(cid),
                      'pic/courses/{0}-thumbnail.png'.format(cid), proxies)
        thumbnail_img = Image.open('pic/courses/{0}-thumbnail.png'.format(cid)).resize((482, 275), Image.ANTIALIAS)
        img.paste(thumbnail_img, (56, 130, 538, 405))
        down_file(response1['uploader']['mii_image'], 'pic/info/{0}-mii.png'.format(response1['uploader']['code']),
                  proxies)
        uploader_img = Image.open('pic/info/{0}-mii.png'.format(response1['uploader']['code'])).resize((70, 70),
                                                                                                       Image.ANTIALIAS)
        r, g, b, a = uploader_img.split()
        img.paste(uploader_img, (570, 170, 640, 240), mask=a)
        if 'first_completer' in response1.keys():
            down_file(response1['first_completer']['mii_image'], 'pic/info/{0}-mii.png'.format(response1['first_completer']['code']),
                      proxies)
            first_img = Image.open('pic/info/{0}-mii.png'.format(response1['first_completer']['code'])).resize(
                (70, 70),
                Image.ANTIALIAS)
            r, g, b, a = first_img.split()
            img.paste(first_img, (90, 900, 160, 970), mask=a)
        if 'record_holder' in response1.keys():
            down_file(response1['record_holder']['mii_image'],
                      'pic/info/{0}-mii.png'.format(response1['record_holder']['code']),
                      proxies)
            record_img = Image.open('pic/info/{0}-mii.png'.format(response1['record_holder']['code'])).resize(
                (70, 70), Image.ANTIALIAS)
            r, g, b, a = record_img.split()
            img.paste(record_img, (575, 900, 645, 970), mask=a)
        draw.text(xy=(190, 890),
                  text=response1['first_completer']['name'] if 'first_completer' in response1.keys() else '--',
                  fill=font_color, font=font)
        draw.text(xy=(680, 890), text='{0}'.format(
            response1['record_holder']['name']) if 'record_holder' in response1.keys() else '--', fill=font_color,
                  font=font)
        draw.text(xy=(115, 25), text=response1['name'], fill=font_color, font=font2)
        draw.text(xy=(680, 150), text=response1['uploader']['name'], fill=font_color, font=font)
        difficulty = response1['difficulty']
        # if response1['uploader']['code'] == '1V2K24M8G':
        #     difficulty = 1
        if difficulty == 0:
            difficulty_name = '简单'
        if difficulty == 1:
            difficulty_name = '普通'
        if difficulty == 2:
            difficulty_name = '困难'
        if difficulty == 3:
            difficulty_name = '极难'
        draw.text(xy=(558, 270), text='难度  {0}'.format(difficulty_name), fill=font_color, font=font)
        draw.text(xy=(558, 310), text='{0} / {1}'.format(response1['clears'], response1['attempts']), fill=font_color,
                  font=font)
        draw.text(xy=(750, 357), text=response1['upload_time_pretty'], fill=font_color, font=font)
        draw.text(xy=(360, 535), text=str(response1['likes']), fill=font_color, font=font)
        draw.text(xy=(600, 535), text='获得点"孬！"数 {0}'.format(response1['boos']), fill=font_color, font=font)
        draw.text(xy=(360, 586), text=str(response1['plays']), fill=font_color, font=font)
        draw.text(xy=(495, 636), text=str(response1['versus_matches']), fill=font_color, font=font)
        draw.text(xy=(600, 636), text='"多人合作"里获得游玩数 {0}'.format(response1['coop_matches']), fill=font_color, font=font)
        if len(response1['tags_name'][0]) > 0:
            draw.text(xy=(150, 685), text=response1['tags_name'][0], fill=font_color, font=font)
        if len(response1['tags_name'][0]) > 1:
            draw.text(xy=(150, 736), text=response1['tags_name'][1], fill=font_color, font=font)
        draw_text_center_withlines(draw, (55, 410), (1015, 520), response1['description'], font, font_color)
        for index, player in enumerate(players):
            if index >= 6:
                fill_img = Image.open('pic/detail-fill.png')
                img.paste(fill_img, (0, 320 + index * h, 1793, (index + 1) * h + 320))
            player_img = Image.open('pic/detail-persionbg.png')
            img.paste(player_img, (1140, 320 + index * h - 3, 1140 + 581, (index + 1) * h + 320 - 3))
            draw.text(xy=(1300, index * h + 338), text=player['name'], fill=font_color, font=font)
            if player['pid'] in response2['cleared']:
                clear_img = Image.open('pic/detail-clear.png')
                img.paste(clear_img, (1140 + 400, 320 + index * h + 8, 1140 + 400 + 42, index * h + 50 + 318))
            if player['pid'] in response2['liked']:
                heart_img = Image.open('pic/detail-heart.png')
                img.paste(heart_img, (1140 + 460, 320 + index * h + 10, 1140 + 460 + 47, index * h + 50 + 320))
        if 'record_holder' in response1.keys():
            draw.text(xy=(680, 998), text=response1['world_record_pretty'], fill=font_color, font=font)
        a = Image.open('pic/datail-footer.png')
        img.paste(a, (0, total_h - 15, 1793, total_h))
        img.save('pic/detail/{0}.png'.format(cid))
        return None
    except Exception as e:
        return str(e)
