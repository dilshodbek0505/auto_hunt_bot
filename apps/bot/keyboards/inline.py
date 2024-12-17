from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from apps.bot.utils.callback_data import *
from apps.bot.models import Brand, CarModel, Detection

from asgiref.sync import sync_to_async



async def get_models():
    car_models = await sync_to_async(list)(CarModel.objects.all())

    return car_models

async def get_detections():
    detections = await sync_to_async(list)(Detection.objects.all())

    return detections


def inline_languages():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="Uzbek🇺🇿", callback_data=cb_select_language_callback_data(lang=SelectLanguage.UZ))
    inline_keyboard.button(text="Russian🇷🇺", callback_data=cb_select_language_callback_data(lang=SelectLanguage.RU))
    inline_keyboard.button(text="English🇺🇸", callback_data=cb_select_language_callback_data(lang=SelectLanguage.EN))

    inline_keyboard.adjust(1)

    return inline_keyboard.as_markup()


async def inline_pagination_keyboard(pagination_data, page: int = 0):
    inline_keyboard = InlineKeyboardBuilder()

    start_offset = page * 5
    end_offset = min(start_offset + 5, len(pagination_data))
    
    for data in pagination_data[start_offset:end_offset]:
        try:
            inline_keyboard.row(InlineKeyboardButton(text=data.name, callback_data=PaginationCallbackData(name= data.slug, page= page).pack()))
        except Exception as err:
            name = f"{data.car_brand.name}({data.car_model.name})"
            if data.is_active:
                inline_keyboard.row(InlineKeyboardButton(text=f"{name}🟢", callback_data=PaginationCallbackData(name= str(data.id), page= page).pack()))
            else:
                inline_keyboard.row(InlineKeyboardButton(text=f"{name}🔴", callback_data=PaginationCallbackData(name= str(data.id), page= page).pack()))

                
    
    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(text="⬅️", callback_data=PaginationCallbackData(name= "previous", page= page - 1).pack())
        )
    
    if end_offset < len(pagination_data):
        buttons_row.append(
            InlineKeyboardButton(text="➡️", callback_data= PaginationCallbackData(name= "next", page= page + 1).pack())
        )
    
    inline_keyboard.row(*buttons_row)


    return inline_keyboard.as_markup()


async def inline_car_brands_pagination_keyboard(page: int = 0):
    brands = await sync_to_async(list)(Brand.objects.all())

    kb = await inline_pagination_keyboard(brands, page)

    return kb


async def inline_car_models_pagination_keyboard(brand_slug, page: int = 0):
    brand = await Brand.objects.filter(slug= brand_slug).afirst()
    car_models = await sync_to_async(list)(CarModel.objects.filter(brand_id=brand.id))
    
    kb = await inline_pagination_keyboard(car_models, page)

    return kb


async def inline_active_detections_pagination_keyboard(telegram_id, page: int = 0):
    detections = await sync_to_async(list)(Detection.objects.filter(user_id = telegram_id).select_related("user", "car_brand", "car_model"))

    kb = await inline_pagination_keyboard(detections, page)

    return kb

async def inline_status_detection(detection=None):
    kb = InlineKeyboardBuilder()
    
    if detection:
        text = "Faolsizlantirish" if detection.is_active else "Faollashtirish"
        kb.button(text=text, callback_data="detection_status")
    
    return kb.as_markup()

    