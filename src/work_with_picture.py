import requests
from PIL import Image, ImageDraw, ImageFont


def make_picture(link, text):
    # TODO: Сделать картинку, если что-то не удалось, вернуть None вместо picture
    im = Image.open(requests.get(link, stream=True).raw)
    size_font = 45
    font = ImageFont.truetype("arial.ttf", size_font)
    drawer = ImageDraw.Draw(im)
    drawer.text((im.size[0]//2 - (size_font // 2)*len(text)//2, im.size[1] - size_font*2), text, font=font, fill='white')

    im.save('new_img.jpg')
    # Указано для проверки, вам само собой нужно указать картинку на вашем ПК
    return open(r'.\new_img.jpg', "rb")
