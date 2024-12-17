import requests


def get_car_post(model_id, brand_id):
    url = f"https://panel.auto.uz/api/v1/car/announcement/web/list/?limit=10&make={brand_id}&model={model_id}&offset=10&ordering=-created_at"

    res = requests.get(url).json()
    data = res['results']

    return data

    


