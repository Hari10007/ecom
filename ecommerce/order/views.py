from django.shortcuts import redirect, render, get_object_or_404
from admin_dashboard.models import Product
from cart.models import Cart, CartItem
from account.models import User, Address
from order.models import Order, OrderItem, Refund
from cart.forms import AddressForm
from order.forms import RefundForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import razorpay
import random

# Create your views here.

def save_pdf(request, order_no):
    order = Order.objects.get(order_number = order_no)
    data={
        'order': order,
        "user" : order.user,
        "order_items": order.order_items.all(),
    }
    response = HttpResponse(content_type='application/pdf')
    filename = "Invoice_" + order_no + ".pdf"
    content = "attachment; filename="+filename
    response['Content-Disposition'] = content
    template = get_template("shop/invoice.html")
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument( BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return response


def index(request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context ={
        'orders': paged_orders
    }
    return render(request, 'shop/order_list.html', context)

def order_details(request, order_no):
    refund_form = RefundForm()
    order = Order.objects.filter(order_number = order_no).filter(user = request.user).first()
    order_items = OrderItem.objects.filter(order = order)
    context = {
        'order': order,
        'order_items': order_items,
        'refund_form': refund_form,
    }
    return render (request, 'shop/order_details.html', context)

def checkout(request, total = 0, quantity = 0, cart_items = None):
    address_form = AddressForm()
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user = request.user)
        else:
            cart = Cart.objects.get(session_id = _cart(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = cart.get_cart_total()

        addresses = Address.objects.filter(user = request.user)
    except ObjectDoesNotExist:
        pass


    context = {
        "cart": cart,
        "total": total,
        "cart_items": cart_items,
        "addresses": addresses,
        "address_form": address_form
    }

    return render(request,"shop/checkout.html", context)

def payment(request):
    cart = Cart.objects.get(user = request.user)
    if cart.cart_items.exists():
        address = Address.objects.get(pk = request.POST['address'])

        context = {
            'address' : address
        }

        return render(request, "shop/payment.html", context)
    else:
        return redirect('cart')

def placeOrder(request):
    cart = Cart.objects.get(user = request.user)
    if request.method =="POST":
        address = Address.objects.get(pk = request.POST.get('address'))
        newOrder = Order()
        newOrder.user = request.user
        newOrder.address = address
        
        newOrder.payment_method = request.POST.get('payment_method')
        
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = cart.get_cart_total()

        order_no = "OD" + str(random.randint(1111111111,9999999999))
        while Order.objects.filter(order_number=order_no) is None:
            order_no = str(random.randint(1111111111,9999999999))
        
        newOrder.order_number = order_no
        newOrder.grand_total = total
        newOrder.save()

        for item in cart.cart_items.all():

            order_item = OrderItem.objects.create(order = newOrder, product = item.product, quantity = item.quantity, price = item.product.price)

            order_product = Product.objects.filter(pk = item.product.pk).first()
            order_product.quantity = order_product.quantity - item.quantity
            order_product.save()

            item.delete()

        cart.coupon = None
        cart.save()

        payment_method = request.POST.get('payment_method')

        if (payment_method == "Paid by Paypal" or payment_method == "Paid by RazorPay"):
            newOrder.transaction_id = request.POST.get('transaction_id')
            newOrder.save()
            return JsonResponse({'status': 'Your order has been placed successfully'})
        else:
            return redirect('thank_you')
        
    return redirect("/")

def razorPay(request):
    user = request.user
    address = Address.objects.get(pk = request.GET.get('address'))
    cart = Cart.objects.get(user = request.user)

    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    client = razorpay.Client(auth=(str(settings.RAZORPAY_API_KEY), str(settings.RAZORPAY_SECRET_KEY)))
    order = client.order.create({"amount": int(cart.get_cart_total()) * 100 ,"currency": "INR"})
    print(order)
    data = {
        "address_id": address.pk,
        "address": address.address,
        "f_name": user.first_name,
        "l_name": user.last_name,
        "email": user.email,
        "ph_no": user.phone_number,
        "order": order
    }
    return JsonResponse(data)


def cancel_order(request, order_no):
    order = Order.objects.get(order_number = order_no)
    if request.method == 'POST':
        refund_form = RefundForm(request.POST)
        if refund_form.is_valid():
            reason = refund_form.cleaned_data['reason']
            refund = Refund.objects.create(user = request.user, order = order, reason = reason)
            order.status = "Cancel"
            order.save()
    
    order_items = OrderItem.objects.filter(order = order)
    context = {
        'order': order,
        'order_items': order_items,
        'refund_form': refund_form,
    }
    return render (request, 'shop/order_details.html', context)

def thankYou(request, order = None):
    if request.user.is_authenticated:
        order = Order.objects.filter(user = request.user).last()
    context = {
        "order": order
    }
    return render(request,"shop/thank_you.html", context)