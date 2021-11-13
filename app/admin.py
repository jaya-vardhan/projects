from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['ordered_date']

admin.site.register(OrderPlaced,OrderPlacedAdmin)