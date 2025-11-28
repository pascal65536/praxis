from extensions import db
from models import City, GeneratedImage
from datetime import datetime, timedelta
import random
import os
from PIL import Image, ImageDraw, ImageFont
import colorsys
from flask import current_app

def populate_sample_data():
    City.query.delete()

    cities = [
        ("Moscow", 0, 30),
        ("Saint Petersburg", -20, 20),
        ("Krasnoyarsk", -25, 20),
        ("Novosibirsk", -15, 25),
        ("Sochi", 5, 35),
        ("Yekaterinburg", -10, 25),
        ("Kazan", -5, 28),
        ("Rostov", -2, 32),
    ]
    start_date = datetime.now() - timedelta(days=365)
    for city in cities:
        for day in range(365):
            date = start_date + timedelta(days=day)
            for measurement in range(12):
                measure_time = date + timedelta(hours=measurement * 2)
                temp = round(random.uniform(city[1], city[2]), 1)
                record = City(city_name=city[0], measure=measure_time, temperature=temp)
                db.session.add(record)
    db.session.commit()


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def generate_artistic_image(color_hex, size=(1080, 1080)):
    image = Image.new("RGB", size, color=hex_to_rgb(color_hex))
    draw = ImageDraw.Draw(image)
    width, height = size
    r, g, b = hex_to_rgb(color_hex)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    complementary_h = (h + 0.5) % 1.0
    analogous1_h = (h + 0.08) % 1.0
    analogous2_h = (h - 0.08) % 1.0
    color2 = hsv_to_hex(complementary_h, s, v)
    color3 = hsv_to_hex(analogous1_h, s, min(v + 0.2, 1.0))
    color4 = hsv_to_hex(analogous2_h, s, max(v - 0.2, 0.8))
    cx, cy = width // 2, height // 2
    cr = min(width, height) // 3
    draw.ellipse(
        [cx - cr, cy - cr, cx + cr, cy + cr], fill=color2, outline=color3, width=10
    )
    ss = cr // 2
    draw.rectangle(
        [cx - ss, cy - ss, cx + ss, cy + ss], fill=color4, outline=color2, width=5
    )
    ts = ss // 2
    draw.polygon(
        [cx, cy - ts, cx - ts, cy + ts, cx + ts, cy + ts],
        fill=color3,
        outline=color4,
        width=3,
    )
    
    font_path = os.path.join(current_app.config["FONT_FOLDER"], "YandexSansDisplay-Regular.ttf")
    try:
        font_size = 100
        font = ImageFont.truetype(font_path, font_size)
        text = f"Color: {color_hex}"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        tw = text_bbox[2] - text_bbox[0]
        draw.text((cx - tw // 2, cy + cr + 30), text, fill=color3, font=font)
    except:
        # Если шрифт не найден, просто пропускаем текст
        pass
    return image


def get_or_create_image(color_hex, check_existing=True):
    color_hex = color_hex.upper()
    if not color_hex.startswith("#"):
        color_hex = "#" + color_hex
    if check_existing:
        existing_image = GeneratedImage.query.filter_by(color_hex=color_hex).first()
        if existing_image:
            return existing_image.filename, True
    filename = f"{color_hex.lstrip('#')}.png"
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    image = generate_artistic_image(color_hex)
    image.save(filepath, "PNG")
    GeneratedImage.query.filter_by(color_hex=color_hex).delete()
    new_image = GeneratedImage(color_hex=color_hex, filename=filename)
    db.session.add(new_image)
    db.session.commit()
    return filename, False