from django.db import models


class Section(models.Model):
    section_name = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.section_name


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    available_quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    price = models.PositiveIntegerField()

    class Meta:
        unique_together = ['item_name', 'section']

    def __str__(self):
        return self.item_name
