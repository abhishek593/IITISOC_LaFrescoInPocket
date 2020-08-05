from django.contrib import admin
from .models import Order
from django.utils.html import format_html


class OrderAdmin(admin.ModelAdmin):
    fields = ['order_id', 'status', 'order_details']
    readonly_fields = ['order_details', ]
    search_fields = ['order_id']
    list_display = ['order_id', 'status', 'total']
    list_filter = ['status', ]

    def order_details(self, obj):
        html = """
            <table style="width:40%">
              <tr>
                <th>Item Name</th>
                <th>Section Name</th>
                <th>Quantity</th>
                <th>Total</th>
              </tr>
        """
        for cart_item in obj.cart.items.all():
            html += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(cart_item.item.item_name, cart_item.item.section.section_name,
                       cart_item.quantity, cart_item.get_price)
        html += """
            <tr>
                <th>Order Total</th>
                <th></th>
                <th></th>
                <th>{}</th>
            </tr>
        """.format(obj.total)
        html += "</table>"
        return format_html(html)
    order_details.short_description = 'Order Details'


admin.site.register(Order, OrderAdmin)
