from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from apps.bot.keyboards.inline import inline_languages
from apps.bot.keyboards.reply import reply_main_menu
from apps.bot.utils.states import RegistrationStateGroup

from django.contrib.auth import get_user_model

router = Router()
User = get_user_model()


@router.message(CommandStart())
async def start_commond(message: types.Message, state: FSMContext):
    user = await User.objects.filter(id = message.from_user.id).afirst()

    if not user:
        await message.answer(text="Iltmos avval regstratsiyadan o'ting", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text="Tilni tanlang:", reply_markup=inline_languages())
        await state.set_state(RegistrationStateGroup.language)
    else:
        await message.answer(f"Botga xush kelibsiz <b>{user.first_name}</b>😊", reply_markup=reply_main_menu())