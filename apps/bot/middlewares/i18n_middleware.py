from typing import Dict, Any
from asgiref.sync import sync_to_async
from apps.bot.utils.callback_data import SelectLanguage

from aiogram.types.base import TelegramObject
from aiogram.utils.i18n import I18nMiddleware
from aiogram.fsm.context import FSMContext
from aiogram import types

from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


EVENT_FROM_USER = "event_from_user"


class CustomI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]):
        user: types.User = data.get(EVENT_FROM_USER)

        telegram_id = user.id
        user_obj = await User.objects.filter(id=telegram_id).afirst()
        
        user_language = cache.get('user_language')
        if not user_language and user_obj:
            
            cache.set('user_language', user_obj.language)
            user_language = user_obj.language
        else:
            cache.set('user_language', SelectLanguage.UZ)

        return user_language if user_language else SelectLanguage.UZ
    


