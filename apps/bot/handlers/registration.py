from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from apps.bot.utils.callback_data import SelectLanguageCallbackData
from apps.bot.utils.states import RegistrationStateGroup
from apps.bot.keyboards.reply import reply_send_phone_number

from django.contrib.auth import get_user_model

User = get_user_model()

router = Router()


@router.callback_query(SelectLanguageCallbackData.filter())
async def receive_language(callback_query: types.CallbackQuery, state: FSMContext, callback_data: SelectLanguageCallbackData):
    await state.update_data({"language": callback_data.language})

    await callback_query.message.answer(f"Telfon raqamingizni jo'nating", reply_markup=reply_send_phone_number())

    await state.set_state(RegistrationStateGroup.phone)


@router.message(F.text, RegistrationStateGroup.phone)
async def receive_phone(message: types.Message, state: FSMContext):
    if not message.text.startswith("+998") or len(message.text) != 13:
        return message.answer("To'g'ri formatda yuboring yoki buttondan foydalaning")

    await state.update_data({"phone_number": message.text})
    await state.set_state(RegistrationStateGroup.name)
    await message.answer("Ismingizni jo'nating", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.contact, RegistrationStateGroup.phone)
async def receive_contact(message: types.Message, state: FSMContext):
    await state.update_data({"phone_number": f"+{message.contact.phone_number}"})
    await state.set_state(RegistrationStateGroup.name)
    await message.answer("Ismingizni jo'nating", reply_markup=types.ReplyKeyboardRemove())
    

@router.message(F.text, RegistrationStateGroup.name)
async def receive_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    registration_data = await state.get_data()

    await message.answer(f"Ma'lumotlaringizℹ️\n\n"
                         f"Ismingiz: <b>{registration_data['name']}</b>\n"
                         f"Telfon raqamingiz📞: <b>{registration_data['phone_number']}</b>\n"
                         f"Tizimdan foydalanish tili🌐: <b>{registration_data['language']}</b>\n")

    await User.objects.acreate(
        id=message.from_user.id, 
        username=message.from_user.username,
        first_name=registration_data["name"],
        phone=registration_data["phone_number"],
        language=registration_data["language"]
    )

    await message.answer("Muvofaqiyatli ro'yxatdan o'tdingiz!")
    await state.clear()



 
