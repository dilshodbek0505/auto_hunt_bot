from celery import shared_task

from apps.user.models import User
from apps.bot.utils.get_posts import get_car_post
from apps.bot.models import Detection
from apps.bot.config.config import BOT_TOKEN

from aiogram.types import Message as message
import requests


url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"


@shared_task
def car_info_periodic_task():
    users = User.objects.filter(is_active = True).all()
    for user in users:
        detections = Detection.objects.filter(user = user, is_active = True)
        for detection in detections:
            data = get_car_post(detection.car_model.model_id, detection.car_brand.brand_id)
            for car in data:
                car_info = f"""Mashina haqida ma'lumot
Nomi: <b>{car['model']['name']} {car['generation']['name']}</b>
Dvigatel turi: <b>{car['engine_type']['type']}</b>
Kuchi: <b>{car['modification_type']['power']}</b>
Narxi: <b>{car['price']} so'm</b>
Yili: <b>{car['year']}</b>
Tarif: <b>{car['description']}</b>

Bog'lanish uchun
Telfon raqami:<b> {car['user']['phone_number']} </b>

"""
                requests.post(
                    url=url,
                    data={
                        "photo": car['gallery'][0],
                        "chat_id": user.id,
                        "caption": car_info,
                        "parse_mode": "html"
                    }

                )
                
    
