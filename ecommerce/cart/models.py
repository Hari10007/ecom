from django.db import models
from admin_dashboard.models import Product, ProductAttribute
from coupon.models import Coupon
from account.models import User

# Create your models here.
class Cart(models.Model):
    session_id = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    coupon =  models.ForeignKey(Coupon, on_delete=models.SET_NULL,null = True, blank = True, related_name="cart_coupons")
    date_added = models.DateTimeField(auto_now_add=True)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price * cart_item.quantity)

        if self.coupon:
            if self.coupon.min_amount < sum(price):
                return sum(price) - self.coupon.amount
        
        return sum(price)

    def __str__(self):
       return str(self.session_id)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products")
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    size = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL,null = True, blank = True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def name(self):
        if self.size.size.title == "Small":
            name = "S"
        elif self.size.size.title == "Medium":
            name = "M"
        elif self.size.size.title == "Large":
            name = "L"
        return name

    
    def __str__(self):
       return str(self.product)
