from django.db import models
from account.models import User

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_expired = models.BooleanField(default =False)
    amount = models.IntegerField(default=10)
    min_amount = models.IntegerField(default=500)
    used =  models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code)

class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="used_coupons")
    coupon =  models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True, related_name="used_coupons")
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.username)