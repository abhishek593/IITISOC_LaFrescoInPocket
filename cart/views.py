from django.shortcuts import render
from inventory.models import Section, Item
from .models import CartItem, Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from cart.utils import represent_int
from django.conf import settings


def get_latest_user_cart(request):
    carts = Cart.objects.filter(user=request.user)
    latest_cart = None
    newly_created_cart = False
    if carts:
        for cart in carts:
            if not cart.is_ordered:
                latest_cart = cart
                break
    if latest_cart is None:
        latest_cart = Cart.objects.create(user=request.user)
        newly_created_cart = True
    return newly_created_cart, latest_cart


def list_items(request):
    sections = Section.objects.all()
    return render(request, 'cart/list_items.html', {'sections': sections})


@login_required
def add_item(request):
    quantity = request.POST['quantity']
    if represent_int(quantity):
        section_name = request.POST['section_name']
        item_name = request.POST['item_name']
        item = Item.objects.filter(section__section_name=section_name, item_name=item_name).first()
        if int(quantity) <= item.available_quantity:
            newly_created_cart, latest_cart = get_latest_user_cart(request)
            cartItems = latest_cart.items.all()
            item_already_added = False
            for cartItem in cartItems:
                if cartItem.item == item:
                    cartItem.quantity = quantity
                    cartItem.save()
                    item_already_added = True
                    break
            if not item_already_added:
                cart_item = CartItem.objects.create(item=item, quantity=quantity)
                latest_cart.items.add(cart_item)
            messages.success(request, '{} is successfully added.'.format(item_name))
        else:
            messages.error(request, 'Please enter a valid quantity.')
            messages.error(request, 'The quantity should be less than or equal to available quantity.')
    else:
        messages.error(request, 'Please enter an integer value.')
    if request.META['HTTP_REFERER'] == '{}://{}/cart/list_items/'.format(settings.PROTOCOL, settings.DOMAIN):
        return redirect('cart:list_items')
    return redirect('cart:show_cart')


@login_required
def remove_item(request):
    section_name = request.POST['section_name']
    item_name = request.POST['item_name']
    item = Item.objects.filter(section__section_name=section_name, item_name=item_name).first()

    newly_created_cart, latest_cart = get_latest_user_cart(request)
    cart_item_to_remove = latest_cart.items.filter(item=item).first()
    latest_cart.items.remove(cart_item_to_remove)
    cart_item_to_remove.delete()
    messages.success(request, '{} was successfully removed.'.format(item_name))
    return redirect('cart:show_cart')


@login_required
def show_cart(request):
    newly_created_cart, latest_cart = get_latest_user_cart(request)
    is_cart_empty = False
    if latest_cart.items.count() == 0:
        is_cart_empty = True
    return render(request, 'cart/show_cart.html', {
        'latest_cart': latest_cart,
        'is_cart_empty': is_cart_empty
    })
