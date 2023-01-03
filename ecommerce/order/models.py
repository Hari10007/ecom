from django.db import models
from account.models import User, Address
from admin_dashboard.models import Product

# Create your models here.

class Order(models.Model):
   payment_method = models.CharField(max_length=100, null = True, blank = True)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   transaction_id = models.CharField(max_length=200, null = True, blank = True)
   orderstatuses =( 
    ('Confirmed','Confirmed'),
    ('Out For Shipping', 'Out For Shipping'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Refunded', 'Refunded'),
   )
   status = models.CharField(max_length=150, choices=orderstatuses, default="Confirmed")
   order_number = models.CharField(max_length=150, null=True)
   grand_total = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
   address = models.ForeignKey(Address, null = True, on_delete=models.CASCADE)

   def __str__(self):
       return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)

    def sub_total(self):
        return self.price * self.quantity

    def __str__(self):
       return str(self.product)

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"