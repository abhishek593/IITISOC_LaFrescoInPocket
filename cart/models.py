from django.db import models
from django.contrib.auth import get_user_model

from inventory.models import Item

User = get_user_model()


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.item.item_name

    @property
    def get_price(self):
        return self.item.price * self.quantity


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
