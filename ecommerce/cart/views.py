from django.shortcuts import redirect, render, get_object_or_404
from admin_dashboard.models import Product, ProductAttribute
from .models import Cart, CartItem
from account.models import Address
from .forms import AddressForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# Create your views here.

def _cart(request):
    session = request.session.session_key
    if not session:
        session = request.session.create()
    return session

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user = request.user)
        else:
            cart = Cart.objects.get(session_id = _cart(request))
    except Cart.DoesNotExist:
        if request.user.is_authenticated:
            cart = Cart.objects.create(session_id = _cart(request), user = request.user)
        else:
            cart = Cart.objects.create(session_id = _cart(request))

    if request.method == "POST":
        size_id = request.POST.get('size')
        product_attribute = ProductAttribute.objects.get(pk = size_id)
        try:
            cart_item = CartItem.objects.get(product = product, cart = cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product, quantity = 1 , cart = cart, size = product_attribute)
            cart_item.save()

    request.session['cart_item'] = cart.cart_items.count()
    return redirect('cart')

def increment_cart(request, total = 0):
        product_id = int(request.GET.get('product_id', None))
        product = Product.objects.get(id = product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.get(user = request.user)
        else:
            cart = Cart.objects.get(session_id = _cart(request))

        cart_item = CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += (item.product.price * item.quantity)
        
        response = {
                'product_id' : product_id,
                'quantity': cart_item.quantity,
                'subtotal': cart_item.sub_total(),
                'total': total
        }

        request.session['cart_item'] = cart.cart_items.count()
        
        return JsonResponse(response)

def decrement_cart(request, total = 0):

    product_id = int(request.GET.get('product_id', None))
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
    else:
        cart = Cart.objects.get(session_id = _cart(request))
    
    cart_item = CartItem.objects.get(product = product, cart = cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    for item in cart_items:
        total += (item.product.price * item.quantity)
    
    response = {
            'product_id' : product_id,
            'quantity': cart_item.quantity,
            'subtotal': cart_item.sub_total(),
            'total': total
    }

    request.session['cart_item'] = cart.cart_items.count()

    return JsonResponse(response)

def remove_cart_item(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
    else:
        cart = Cart.objects.get(session_id = _cart(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()

    request.session['cart_item'] = cart.cart_items.count()
    return redirect('cart')


def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user = request.user)
        else:
            cart = Cart.objects.get(session_id = _cart(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items
    }
    return render(request,"shop/cart.html", context)

def add_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            addr = address_form.cleaned_data['address']
            city = address_form.cleaned_data['city']
            country = address_form.cleaned_data['country']
            postal_code = address_form.cleaned_data['postal_code']
            address = Address.objects.create(user = request.user, address = addr, city = city, country = country, postal_code = postal_code)
    return redirect('checkout')

def payment(request):

    return render(request, "shop/payment.html")