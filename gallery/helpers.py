from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw
import random


def custom_captcha_image(text):
    img = Image.new('RGB', (200, 70), color='#003366')
    draw = ImageDraw.Draw(img)
    font_size = random.randint(35, 45)

    # Рисуем текст со случайными смещениями
    for i, char in enumerate(text):
        draw.text(
            (20 + i * 30 + random.randint(-5, 5),
             15 + random.randint(-5, 5)),
            char, fill='#FFCC00'
        )

    # Добавляем шум
    for _ in range(100):
        x, y = random.randint(0, 200), random.randint(0, 70)
        draw.point((x, y), fill='#FFFFFF')

    # Размытие и искажение
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img