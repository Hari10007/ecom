from django.shortcuts import redirect, render, get_object_or_404
from .models import Coupon, UsedCoupon
from cart.models import Cart
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Create your views here.

def apply_coupon(request):
    if request.method == 'POST':
        code =  request.POST['coupon']
        try:
            coupon = Coupon.objects.get(code__iexact = code) 
            cart = Cart.objects.get(user = request.user)

            if cart.coupon:
                messages.warning(request,'Coupon Applied')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart.get_cart_total() < coupon.min_amount:
                messages.warning(request, f'Amount should be greater than { coupon.min_amount }')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon.is_expired:
                messages.warning(request,'Coupon expired')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except ObjectDoesNotExist:
             messages.warning(request,'Invalid Coupon.')
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        try:
            used_coupon = UsedCoupon.objects.get(user = request.user,coupon = coupon)
            if used_coupon.status:
                messages.warning(request,'Coupon Already Used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                used_coupon.status = True
                used_coupon.save()
        except ObjectDoesNotExist:
            used_coupon = UsedCoupon.objects.create(user = request.user,coupon = coupon)

        coupon.used += 1
        coupon.save()
        cart.coupon = coupon
        cart.save()
        

        messages.success(request, 'Coupon applied')        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request, cart_id):
    cart =  Cart.objects.get(id = cart_id)
    coupon = cart.coupon
    coupon.used -= 1
    coupon.save()
    
    used_coupon = UsedCoupon.objects.get(user = request.user,coupon = coupon)
    used_coupon.status = False
    used_coupon.save()

    cart.coupon = None
    cart.save()

    messages.success(request, 'Coupon removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))