from django.shortcuts import redirect, render
from admin_dashboard.models import Product, Category, Brand, Size
from account.models import User
from cart.models import Cart
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def homepage(request):  
    kids_category = Category.objects.get(slug="kids-clothing")
    men_category = Category.objects.get(slug="mens-clothing")
    women_category = Category.objects.get(slug="womens-clothing")

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user = request.user)
            request.session['cart_item'] = cart.cart_items.count()
    except Cart.DoesNotExist:
        request.session['cart_item'] = 0

    context = {
        "men_category": men_category,
        "women_category": women_category,
        "kids_category": kids_category
    }

    return render(request,"shop/home.html",context)

def search_results(request):
    if request.is_ajax():
        res = None
        value = request.POST.get('product')
        products = Product.objects.filter(name__icontains = value)
        if len(products) > 0 and len(value) > 0 :
            data = []
            for product in products:
                item = {
                    'id': product.pk,
                    'name': product.name,
                    'image': str(product.image.url),
                    "slug": product.slug,
                }
                data.append(item)
            res = data
            print(res)
        else:
            res = 'No products found ... '

        return JsonResponse({'data': res})
    return JsonResponse({})

def product_list(request, slug):
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category__in=category.get_descendants(include_self=True)).order_by('name')
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "products": paged_products,
        "category": category,
        "sizes": sizes,
        "brands": brands,
    }
    return render(request,"shop/product_list.html", context)


def product_view(request, slug):
    product = Product.objects.get(slug=slug)
    products = product.category.products.filter(~Q(slug=slug)).order_by("-id")[:4]
    context = {
        "product": product,
        "products": products,
        "category": product.category
    }
    return render(request,"shop/product_view.html", context)

def filter_data(request):
    brands=request.GET.getlist('_filterObj[brand][]')
    sizes=request.GET.getlist('_filterObj[size][]')
    slug=request.GET.get('slug')
    category = Category.objects.get(slug=slug)
    allProducts = Product.objects.filter(category__in=category.get_descendants(include_self=True)).order_by('name').distinct()
    #allProducts=Product.objects.all().order_by('-id').distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('shop/ajax/filter_product_list.html',{'products':allProducts})
    return JsonResponse({'data':t})
