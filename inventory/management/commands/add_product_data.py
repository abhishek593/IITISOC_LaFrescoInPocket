from django.core.management.base import BaseCommand
import json
from inventory.models import Item, Section


class Command(BaseCommand):
    help = 'Adds initial data for items and sections '

    def handle(self, *args, **options):
        with open('product_dataset.json') as f:
            data = json.load(f)

        for collection in data:
            section = Section.objects.create(section_name=collection['section'])
            items = collection['items']
            for item in items:
                Item.objects.create(item_name=item['item'], section=section,
                                    available_quantity=item['available_quantity'],
                                    price=item['price'])
        f.close()
