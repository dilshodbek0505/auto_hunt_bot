import requests

from django.core.management import BaseCommand

from apps.bot.models import Brand, CarModel


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            brands = Brand.objects.all()

            for brand in brands:
                url = f"https://panel.auto.uz/api/v1/car/{brand.brand_id}/models/?limit=100"
                res = requests.get(url)

                content = res.json()
                data = content['results']

                car_model_obj = [CarModel(name= car_model['name'], model_id= car_model['id'], brand= brand) for car_model in data]
                CarModel.objects.bulk_create(car_model_obj)
            
            self.stdout.write(self.style.SUCCESS("Modellar yaratildi"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Quydagicha xatolik sodir bo'ldi: {str(err)}"))
        
    