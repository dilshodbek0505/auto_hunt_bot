from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from apps.bot.utils.states import ActiveDetectionStateGroup
from apps.bot.models import Detection
from apps.bot.keyboards.inline import *
from apps.bot.utils.callback_data import PaginationCallbackData

router = Router()



@router.message(F.text == "Faol detektsiyalar🟢")
async def active_detections_list(message: types.Message, state: FSMContext):
    reply_markup = await inline_active_detections_pagination_keyboard(telegram_id= message.from_user.id)

    await message.answer("Faol deteksiyalar ro'yxati", reply_markup=reply_markup)
    await state.set_state(ActiveDetectionStateGroup.detections_list)


@router.callback_query(PaginationCallbackData.filter(), ActiveDetectionStateGroup.detections_list)
async def active_detections_list_callback(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):

    if callback_data.name == 'next' or callback_data.name == 'previous':
        reply_markup = await inline_active_detections_pagination_keyboard(page= int(callback_data.page), telegram_id= callback_query.from_user.id)
        await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await callback_query.answer(cache_time=0)
        await state.update_data({"detection_id": callback_data.name})
        await state.set_state(ActiveDetectionStateGroup.detection_detail)


@router.callback_query(PaginationCallbackData.filter(), ActiveDetectionStateGroup.detection_detail)
async def active_detections_detail_callback(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData, state: FSMContext):
    data = await state.get_data()
    detection_id = data['detection_id']
    detection = await Detection.objects.filter(id = detection_id).select_related('user', 'car_model', 'car_brand').afirst()
    text = f"""Deteksiya haqida ma'lumot:
Brand: <b>{detection.car_brand.name}</b>
Model: <b>{detection.car_model.name}</b>
Holati: {"🟢" if detection.is_active else "🔴"}
"""

    replay_keyboard = await inline_status_detection(detection)
    await callback_query.answer(cache_time=0)
    await callback_query.message.edit_text(text, reply_markup=replay_keyboard)


@router.callback_query(ActiveDetectionStateGroup.detection_detail)
async def active_detection_status_callback(callback_query: types.CallbackQuery, state: FSMContext):
   
    if callback_query.data == 'detection_status':
        data = await state.get_data()
        detection = await Detection.objects.filter(id = data['detection_id']).select_related('user', 'car_model', 'car_brand').afirst()
        
        detection.is_active = not detection.is_active
        await detection.asave()
        await callback_query.answer(cache_time=0)
    
    reply_markup = await inline_active_detections_pagination_keyboard(telegram_id=callback_query.from_user.id)

    await callback_query.message.edit_text("Deteksiya holati o'zgartirildi!", reply_markup=reply_markup)
    await state.set_state(ActiveDetectionStateGroup.detections_list)

