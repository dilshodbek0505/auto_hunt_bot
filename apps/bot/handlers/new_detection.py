from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from apps.bot.utils.states import NewDetectionStateGroup
from apps.bot.keyboards.inline import *
from apps.bot.utils.callback_data import *
from apps.bot.utils.get_posts import *
from apps.bot.keyboards.reply import reply_new_detections, reply_main_menu
from apps.bot.models import Detection, CarModel, Brand
from apps.user.models import User


router = Router()


@router.message(F.text == 'Yangi detektsiya yaratish➕')
async def new_detektions(message: types.Message, state: FSMContext):
    reply_markup = await inline_car_brands_pagination_keyboard()

    await message.answer("Brand nomni tanlang:", reply_markup=reply_markup)
    await state.set_state(NewDetectionStateGroup.brand)


@router.callback_query(NewDetectionStateGroup.brand, PaginationCallbackData.filter())
async def brands_pagination_callback(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):
    
    if callback_data.name == 'next' or callback_data.name == 'previous':
        reply_markup = await inline_car_brands_pagination_keyboard(page= int(callback_data.page))
        await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await callback_query.answer(cache_time=0)    
        await state.update_data({'brand': callback_data.name})
        reply_markup = await inline_car_models_pagination_keyboard(brand_slug=callback_data.name)
        await callback_query.message.answer("Brand modelini tanlang: ", reply_markup=reply_markup)
        await state.set_state(NewDetectionStateGroup.model)
         

@router.callback_query(NewDetectionStateGroup.model, PaginationCallbackData.filter())
async def models_pagination_callback(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):
    data = await state.get_data()
    brand_name = data['brand']

    if callback_data.name == 'next' or callback_data.name == 'previous':
        reply_markup = await inline_car_models_pagination_keyboard(page= int(callback_data.page), brand_slug=brand_name)
        await callback_query.message.edit_reply_markup(reply_markup=reply_markup)    
    else:
        await callback_query.answer(cache_time=0)
        await state.update_data({'car_model': callback_data.name})
        await callback_query.message.answer("Quydagi menulardan birini tanlang: ", reply_markup=reply_new_detections())
        await state.set_state(NewDetectionStateGroup.confirm)


@router.message(F.text == 'Bosh menuga qaytish🏠', NewDetectionStateGroup.confirm)
async def back_main_menu_in_detection(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh menu", reply_markup=reply_main_menu())


@router.message(F.text == 'Deteksiya yaratish✅', NewDetectionStateGroup.confirm)
async def create_detection(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    car_model = await CarModel.objects.aget(slug = data['car_model'])
    car_brand = await Brand.objects.aget(slug = data['brand'])

    await Detection.objects.acreate(
        user = await User.objects.aget(id = message.from_user.id),
        car_model = car_model,
        car_brand = car_brand
    )
    
    car_data = await get_car_post(model_id=car_model.model_id, brand_id=car_brand.brand_id)

    if car_data != []:
        for car in car_data:
            
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
            photo_url = car['gallery'][0]
            photo = types.URLInputFile(photo_url)

            await message.answer_photo(photo, caption=car_info)


    await message.answer("Deteksiya yaratildi✅")
    await state.clear()
    await message.answer("Bosh menu", reply_markup=reply_main_menu())
