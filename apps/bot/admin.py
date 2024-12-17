from django.contrib import admin

from .models import Brand, CarModel, Detection




@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")


@admin.action(description="Update slugs for all CarModel objects")
def update_slugs(modeladmin, request, queryset):
    queryset = CarModel.objects.all()
    for obj in queryset:
        obj.save()
    
    modeladmin.message_user(request, f"{queryset.count()} objects updated successfully")


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand")
    list_display_links = ("id", "name") 
    actions = [update_slugs]
    search_fields = ("model_id",)

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car_brand", "car_model", "is_active")
    list_display_links = ("id", "user")
    list_filter = ("is_active", )