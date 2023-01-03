from .models import Product, Category

def subject_renderer(request):
   return {
       'main_categories': Category.objects.filter(parent=None).order_by('name')
   }