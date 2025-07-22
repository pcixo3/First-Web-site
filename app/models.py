from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Car(models.Model):
    title = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='media/car_image', blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()

    def __str__(self):
        return self.title



