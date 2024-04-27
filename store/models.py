from django.db import models
from uuid import uuid4
import datetime
from datetime import timezone
from django.conf import settings
from django.contrib import admin


class Collection(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    title = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Promotion(models.Model):
    PENDING = "pending"
    LIVE = "live"
    ENDED = "ended"
    PAUSED = "paused"

    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    description = models.TextField()
    discount = models.FloatField()
    start_date = models.DateTimeField(default = datetime.datetime.now)
    end_date = models.DateTimeField(null = True)
    paused = models.BooleanField(default=False)
    def status(self):
        expired = self.end_date and self.end_date < datetime.datetime.now(timezone.utc)
        pending = self.start_date > datetime.datetime.now(timezone.utc)

        if expired:
            return self.ENDED

        if pending:
            return self.PENDING

        if self.paused:
            return self.PAUSED

        return self.LIVE



class Product(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    title = models.CharField(max_length = 255)
    unit_price = models.DecimalField(max_digits= 6, decimal_places = 2)
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete = models.PROTECT, related_name='products')
    quantity = models.FloatField()
    # promotions = models.ManyToManyField(Promotion)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to ='store/images')


class Customer(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    birth_day = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length = 255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

class Address(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)

    customer = models.ForeignKey(
        Customer, null=False, on_delete = models.CASCADE, related_name="addresses")
    is_shipping = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    street1 = models.CharField(max_length=100, null=True)
    apartment_no = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    country_code = models.CharField(max_length=3, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    

class Order(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

    PAYMENT_STATUS_CHOICES = {
        PENDING : "pending",
        COMPLETED : "completed",
        FAILED : "failed",
    }
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING,
    )
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    order = models.ForeignKey(Order, on_delete = models.PROTECT, related_name='items')
    quantity= models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits= 6, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Cart(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)



class CartItem(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name='items')
    quantity= models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['cart', 'product']]

class Review(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 





    