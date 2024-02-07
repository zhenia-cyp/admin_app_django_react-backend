from django.db import models


class OrderedModel(models.Model):
    order_num = models.BigIntegerField(blank=True, null=True)
    class Meta:
        abstract = True

    @classmethod
    def assign_order_numbers(cls):
        objects = cls.objects.all().order_by('id')
        for index, obj in enumerate(objects, start=1):
            obj.order_num = index
            obj.save()


class Product(OrderedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
