from django.contrib import admin
from .models import Coupon, UsedCoupon
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','amount']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)
admin.site.register(UsedCoupon)


