from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


# class Category(models.Model):
#     name = models.CharField( max_length=255, unique=True)
#     image = models.ImageField(upload_to="category", blank=True)
#     parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
#     slug = models.SlugField( null = True, unique=True)
#     description = models.TextField(null = True, blank = True)
#     created = models.DateTimeField( auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         unique_together = ('slug', 'parent',)    
#         verbose_name_plural = "categories"     

#     def __str__(self):                           
#         full_path = [self.name]                  
#         k = self.parent
#         while k is not None:
#             full_path.append(k.name)
#             k = k.parent
#         return ' -> '.join(full_path[::-1])  

class Category(MPTTModel):
    name = models.CharField( max_length=255, unique=True)
    image = models.ImageField(upload_to="category", blank=True)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField( max_length=255, null = True, unique=True)
    description = models.TextField(null = True, blank = True)
    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
         return reverse('products-by-category', args=[str(self.slug)])

class Brand(models.Model):
    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=TreeForeignKey(Category,  on_delete=models.CASCADE, related_name='products')
    name=models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null = True, blank = True, related_name='products')
    slug=models.SlugField(max_length=200, null = True, unique=True)
    image=models.ImageField(upload_to='product',blank=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    quantity =  models.IntegerField(blank=True, null=True)
    is_featured=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_details', args=[self.id,self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Sizes'

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_attributes")
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity =  models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural='ProductAttributes'

    def name(self):
        if self.size == "Small":
            name = "S"
        elif self.size == "Medium":
            name = "M"
        elif self.size == "Large":
            name = "L"
        return name

    def __str__(self):
        return str(self.size.title)
