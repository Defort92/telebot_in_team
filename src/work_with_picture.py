import requests
from PIL import Image, ImageDraw, ImageFont
from messages_text import INCORRECT_PICTURE, INCORRECT_LINK
from requests.exceptions import MissingSchema


def make_picture(link, text):
    try:
        im = Image.open(requests.get(link, stream=True).raw)
        size_font = 45
        font = ImageFont.truetype("arial.ttf", size_font)
        drawer = ImageDraw.Draw(im)
        drawer.text((im.size[0]//2 - (size_font // 2)*len(text)//2, im.size[1] - size_font*2), text, font=font, fill='white')

        im.save('new_img.jpg')
        return open(r'.\new_img.jpg', "rb"), "OK"

    except MissingSchema:
        return None, INCORRECT_LINK

    except ValueError:
        return None, INCORRECT_PICTURE


