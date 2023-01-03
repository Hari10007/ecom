from django.contrib import admin
from .models import Category, Product, ProductImage ,Size ,Brand ,ProductAttribute
from mptt.admin import MPTTModelAdmin

admin.site.register(Category , MPTTModelAdmin) 
# Register your models here.

# class CategoryAdmin(MPTTModelAdmin):
#     list_display = ("name","slug","parent", "description",)
#     prepopulated_fields = {"slug": ("name",)}
# admin.site.register(Category, CategoryAdmin)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    list_display=['image','product']


class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','category','price','available','created','updated','quantity']
    list_filter=['available','created','updated','category']
    list_editable=['available']
    prepopulated_fields={'slug':('name',)}
    inlines = [ProductImageAdmin]
admin.site.register(Product, ProductAdmin)

admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(ProductAttribute)  
