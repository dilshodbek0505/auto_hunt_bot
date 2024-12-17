import requests

from django.core.management import BaseCommand

from apps.bot.models import Brand


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        url = "https://panel.auto.uz/api/v1/car/makes/top/?limit=200"
        res = requests.get(url)

        content = res.json()
        data = content['results']
        try:
            brand_obj = [Brand(name= brand['name'], slug= brand['slug'], brand_id= brand['id']) for brand in data]
            Brand.objects.bulk_create(brand_obj)
            
            self.stdout.write(self.style.SUCCESS("Brandlar yaratildi"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Quydagicha xatolik sodir bo'ldi: {str(err)}"))
        
    