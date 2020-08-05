from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, primary_key=True)
    order_id = models.CharField(max_length=40)
    ORDER_STATUS_CHOICES = [
        ('created', 'Created'),
        ('prepared', 'Prepared'),
        ('paid', 'Paid'),
        ('cancelled_by_user', 'Cancelled By User'),
        ('cancelled_by_admin', 'Cancelled By Admin')
    ]
    previous_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='created')
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='created')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return self.order_id

    def get_human_rep_of_status(self):
        for status in self.ORDER_STATUS_CHOICES:
            if self.status == status[0]:
                return status[1]
        return None


def add_items_back(instance):
    for cart_item in instance.cart.items.all():
        cart_item.item.available_quantity += cart_item.quantity
        cart_item.item.save()


@receiver(post_save, sender=Order)
def send_order_mail(sender, instance, created, **kwargs):
    if instance.previous_status != instance.status:
        if instance.status == 'created':
            subject = 'LaFresco Order received.'
            message = """
                Your order has been received by LaFresco Team.
                We are working on it and will notify you when the order is completed.
                Here is the ORDER_ID {} which you can use to contact us in case of any query.
                Happy Shopping!.
            """.format(instance.order_id)
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.cart.user.email], fail_silently=False)

        elif instance.status == 'prepared':
            subject = 'LaFresco Order prepared.'
            message = """
                Your order has been prepared by LaFresco Team.
                In case You don't have your ORDER_ID, here it is {}.
                Happy Shopping!.
            """.format(instance.order_id)
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.cart.user.email], fail_silently=False)

        elif instance.status == 'cancelled_by_user':
            subject = 'LaFresco Order Cancelled by you.'
            message = 'Your order with ORDER_ID {} has been successfully cancelled.'.format(instance.order_id)
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.cart.user.email], fail_silently=False)
            add_items_back(instance)

        elif instance.status == 'cancelled_by_admin':
            subject = 'LaFresco Order Cancelled by store.'
            message = """
                Your order with ORDER_ID {} has been cancelled due to some issues.
                We deeply regret the inconvenience caused.
            """.format(instance.order_id)
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.cart.user.email], fail_silently=False)
            add_items_back(instance)
        instance.previous_status = instance.status
        instance.save()
