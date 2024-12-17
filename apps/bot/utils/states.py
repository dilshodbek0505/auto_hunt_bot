from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGroup(StatesGroup):
    language = State()
    phone = State()
    name = State()

class MainMenuStateGroup(StatesGroup):
    create_new_detection = State()
    active_detections = State()
    settings = State()

class NewDetectionStateGroup(StatesGroup):
    brand = State()
    model = State()
    confirm = State()
    # filter uchun 
    auto_color = State()
    auto_year_of_manufacture = State()
    auto_distance_traveled = State()

class ActiveDetectionStateGroup(StatesGroup):
    detections_list = State()
    detection_detail = State()
    edit_filter = State()
    # filter uchun 
    auto_color = State()
    auto_year_of_manufacture = State()
    auto_distance_traveled = State()

class SettingsStateGroup(StatesGroup):
    langage = State()
