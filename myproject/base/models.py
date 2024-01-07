from django.db import models

# Create your models here.


class Item(models.Model):
    order_id = models.IntegerField()
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


