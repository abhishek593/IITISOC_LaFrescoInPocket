from django.shortcuts import render
from .utils import get_random_string
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from django.contrib import messages
from .models import Order
from django.shortcuts import redirect


@login_required
def confirm_place_order(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False)
    if cart.first() is not None:
        cart = cart.first()
        unique_order_id = get_random_string()
        qs = cart.items.all()
        total = 0
        for cart_item in qs:
            total += cart_item.get_price
        order = Order.objects.create(cart=cart, order_id=unique_order_id, total=total)
        for cart_item in cart.items.all():
            cart_item.item.available_quantity -= cart_item.quantity
            cart_item.item.save()
        if order is not None:
            cart.is_ordered = True
            cart.save()
        return render(request, 'orders/unique_order_id_view.html', {'order_id': unique_order_id})
    return redirect('cart:list_items')


@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False)
    if cart is not None:
        cart = cart.first()
        items = cart.items.all()
        total = 0
        for cart_item in items:
            total += cart_item.get_price
        return render(request, 'orders/place_order.html', {'items': items, 'total': total})
    else:
        messages.error(request, 'Please add some items to your cart and then proceed to buy.')
    return render(request, 'orders/place_order.html')


@login_required
def all_orders(request):
    orders = Order.objects.filter(cart__user=request.user)
    return render(request, 'orders/all_orders.html', {'orders': orders})
