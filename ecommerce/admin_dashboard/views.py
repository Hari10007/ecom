from django.shortcuts import redirect, render
from .models import Product, Category, ProductImage
from account.models import User
from order.models import Order, OrderItem
from .forms import ProductForm, ProductImageForm, CategoryForm, DateForm
from order.forms import OrderForm
from django.contrib import messages
from django.template import loader
from django.template.defaultfilters import slugify
from .decorators import user_is_admin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse
from django.conf import settings
import razorpay
import xlwt
import calendar

# Create your views here.
@user_is_admin
def admin_dashboard(request):
    orders_month = Order.objects.annotate(month=ExtractMonth("created_at")).values("month").annotate(count=Count('id')).values('month','count')
    months=[]
    total_orders = []
    for order in orders_month:
        months.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    orders = Order.objects.order_by('-created_at')[:2]
    users = User.objects.filter(is_staff = False, is_admin = False, is_superuser = False).order_by('-date_joined')[:5]
    context = {
        'total_orders': total_orders,
        'months' : months,
        'orders' : orders,
        'users' : users
    }
    return render(request,"admin_dashboard/dashboard.html", context)

@user_is_admin
def category_list(request):
    categories = Category.objects.all().order_by('-created')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        categories = categories.filter(Q(name__icontains = keyword) | Q(description__icontains = keyword) | Q(parent__name__icontains = keyword)).order_by('-created')
    paginator = Paginator(categories, 8)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    content = {
        'categories': paged_categories
    }
    return render(request,"admin_dashboard/category.html", content)

@user_is_admin
def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            messages.success(request, "Category Created")
            return redirect('category_list')
        else:
            messages.error(request,"Category creation failed ")

    context ={
        'category_form':form
    }

    return render(request,"admin_dashboard/category_create.html", context)
@user_is_admin
def category_update(request, category_id):
    category = Category.objects.get(id = category_id)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category Updated Successfully')
            return redirect(to='category_list')
    else:
        category_form = CategoryForm(instance=category)
        
    return render(request,"admin_dashboard/category_update.html",  {'category_form': category_form})
@user_is_admin
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        render(request, 'admin_dashboard/category.html')
    return redirect(to='category_list')

@user_is_admin
def product_list(request):
    products = Product.objects.all().order_by('-created')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        products = products.filter(Q(name__icontains = keyword) | Q(category__name__icontains = keyword) | Q(description__icontains = keyword)).order_by('-created')
    paginator = Paginator(products, 7)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    content ={
        'products': paged_products
    }
    return render(request,"admin_dashboard/product.html", content)

@user_is_admin
def product_create(request):
    product_form = ProductForm()
    product_image_form = ProductImageForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST or None, request.FILES or None)
        product_image_form = ProductImageForm(request.POST or None, request.FILES or None)
        images = request.FILES.getlist('image')
        if product_form.is_valid():
            name = product_form.cleaned_data['name']
            category = product_form.cleaned_data['category']
            main_image = product_form.cleaned_data['main_image']
            description = product_form.cleaned_data['description']
            price = product_form.cleaned_data['price']
            quantity = product_form.cleaned_data['quantity']
            available = product_form.cleaned_data['available']
            product = Product.objects.create(name=name, category=category, image=main_image, description=description, price=price, available=available, quantity = quantity)

            for image in images:
                ProductImage.objects.create(product=product, image=image)
            messages.success(request, "Product Created")
            return redirect('product_list')
        else:
            messages.error(request,"Product creation failed ")

    context ={
        'product_form': product_form,
        'product_image_form': product_image_form
    }

    return render(request,"admin_dashboard/product_create.html", context)

@user_is_admin
def product_update(request, product_id):
    product = Product.objects.get(id = product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product Updated Successfully')
            return redirect(to='product_list')
    else:
        product_form = ProductForm(instance=product)
        
    return render(request,"admin_dashboard/product_update.html",  {'product_form': product_form})

@user_is_admin
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        render(request, 'admin_dashboard/product.html')
    return redirect(to='product_list')

@user_is_admin
def customer_list(request):
    customers = User.objects.filter(is_staff=False, is_admin=False, is_superuser=False).order_by('-date_joined')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        customers = customers.filter(Q(username__icontains = keyword) | Q(email__icontains = keyword)).order_by('-date_joined')
    paginator = Paginator(customers, 7)
    page = request.GET.get('page')
    paged_customers = paginator.get_page(page)
    content ={
        'customers': paged_customers
    }
    return render(request,"admin_dashboard/customer.html", content)

@user_is_admin
def customer_block(request, customer_id):
    customer = User.objects.get(id=customer_id)
    if request.method == 'POST':
        if customer.is_active:
            customer.is_active = False
        else:
            customer.is_active = True
        customer.save()
        render(request, 'admin_dashboard/product.html')
    return redirect(to='customer_list')


@user_is_admin
def order_list(request):
    date_form = DateForm()
    orders = Order.objects.all().order_by('-created_at')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        orders = orders.filter(Q(status__icontains = keyword) | Q(user__username__icontains = keyword) | Q(payment_method__icontains = keyword)).order_by('-created_at')
    paginator = Paginator(orders, 15)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    content ={
        'orders': paged_orders,
        'date_form': date_form
    }
    return render(request,"admin_dashboard/order.html", content)

@user_is_admin
def order_update(request, order_id):
    order = Order.objects.get(pk = order_id)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()
    else:
        order_form = OrderForm(instance=order)
    
    order_items = OrderItem.objects.filter(order = order)
    context = {
        'order': order,
        'order_items': order_items,
        'order_form': order_form
    }
    return render (request, 'admin_dashboard/order_update.html', context)

@user_is_admin
def refund(request, order_no):
    order = Order.objects.get(order_number = order_no)
    payment_id = order.transaction_id

    if order.payment_method == "Paid by RazorPay":
        client = razorpay.Client(auth=(str(settings.RAZORPAY_API_KEY), str(settings.RAZORPAY_SECRET_KEY)))
        res = client.payment.refund(payment_id,{
            "amount": int(order.grand_total) * 100,
            "speed": "normal",
            "notes": {"notes_key_1": "Sorry for the delay", "notes_key_2": "Done"},
            "receipt": payment_id + "0001",},)
        print(res)
        order.status = "Refunded"
        order.save()
    order_form = OrderForm(instance=order)

    order_items = OrderItem.objects.filter(order = order)
    
    context = {
        'order': order,
        'order_items': order_items,
        'order_form': order_form
    }
    return render (request, 'admin_dashboard/order_update.html', context)

@user_is_admin
def export_sales_xls(request, month=None, year = None):
    date_form = DateForm()
    if request.method == 'POST':
        date_form = DateForm(request.POST)
        if date_form.is_valid():
            month = date_form.cleaned_data['month']
            year = date_form.cleaned_data['year']
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="sales{year}{month}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Order Items', 'User', 'Grand Total', 'Payment Method', 'Status',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    if not month and not year:
        rows = Order.objects.all().values_list('order_items','user', 'grand_total', 'payment_method', 'status')
    elif not year:
        rows = Order.objects.all().values_list('order_items','user', 'grand_total', 'payment_method', 'status').filter(created_at__month = month)
    elif not month:
        rows = Order.objects.all().values_list('order_items','user', 'grand_total', 'payment_method', 'status').filter(created_at__year = year)
    else:
        rows = Order.objects.all().values_list('order_items','user', 'grand_total', 'payment_method', 'status').filter(Q(created_at__month = month) | Q(created_at__year = year))
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 0:
                items = OrderItem.objects.get(pk = row[col_num])
                ws.write(row_num, col_num, items.product.name, font_style)
            elif col_num == 1:
                user = User.objects.get(pk = row[col_num])
                name = user.first_name+" "+user.last_name
                ws.write(row_num, col_num, name, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response