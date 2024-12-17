from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.common.models import BaseModel
from apps.user.models import User



class Brand(BaseModel):
    name = models.CharField(max_length=128, help_text=_("Name"))
    slug = models.SlugField(unique=True, help_text=_("Slug"))
    brand_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class CarModel(BaseModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, help_text=_("Slug"), blank=True, null=True)
    model_id = models.PositiveIntegerField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_models')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug

            while self.__class__.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{self.model_id}"
            
            self.slug = unique_slug
                
        super().save(*args, **kwargs)

class Detection(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f"{self.user} - {self.car_brand.name}({self.car_model.name})"
    