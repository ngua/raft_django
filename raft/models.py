from django.db import models
from djmoney.models.fields import MoneyField


class Category(models.Model):
    name = models.CharField(max_length=200)
    picture_path = models.CharField(max_length=50)

    @property
    def services_sorted(self):
        return self.service_set.order_by('price')

    @property
    def short_name(self):
        return self.name.split(' ')[0].lower()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = MoneyField(max_digits=19, decimal_places=0, default_currency='VND')

    def __add__(self, other):
        return self.price + other.price

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}, {self.price}')"

    def __str__(self):
        return f'{self.name}: {self.price}'
