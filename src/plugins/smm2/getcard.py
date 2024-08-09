from PIL import Image, ImageDraw, ImageFont
from .downfile import down_file


def get_card(avatar, bg, nickname, qid, sw, id):
    im_bg = Image.open('pic/card{0}.png'.format(bg))
    down_file(avatar, 'pic/card/{0}-avatar.png'.format(qid))
    # im_avatar = Image.open('pic/card/{0}-avatar.png'.format(qid)).resize((150, 150), Image.LANCZOS)
    # im_bg.paste(im_avatar, (150, 100, 300, 250))
    font1 = ImageFont.truetype('pic/simkai.ttf', size=80)
    font2 = ImageFont.truetype('pic/simkai.ttf', size=60)
    font3 = ImageFont.truetype('pic/simkai.ttf', size=70)
    font_color = (250, 250, 250)
    draw = ImageDraw.Draw(im_bg)
    # draw.text(xy=(310, 100), text=nickname, fill=font_color, font=font1)
    # draw.text(xy=(320, 195), text=qid, fill=font_color, font=font2)
    draw.text(xy=(160, 360), text='SW: {0}'.format(sw), fill=font_color, font=font3)
    draw.text(xy=(160, 435), text='ID: {0}'.format(id), fill=font_color, font=font3)
    im_bg.save('pic/card/{0}-card.png'.format(qid))
