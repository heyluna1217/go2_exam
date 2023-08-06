from django.db import models


class Order(models.Model):
    name = models.CharField()
    sku = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    # status = models.BooleanField()d

    # created = models.DateTimeField(auto_now_add=True)
    # title = models.CharField(max_length=100, blank=True, default='')
    # code = models.TextField()
    # linenos = models.BooleanField(default=False)
    # language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    # style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    # class Meta:
    #     ordering = ['created']
