from django.db import models
from uuid import uuid4
import datetime
from datetime import timezone

class Category(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    title = models.CharField(max_length = 255)


class Promotion(models.Model):
    PENDING = "pending"
    LIVE = "live"
    ENDED = "ended"
    PAUSED = "paused"

    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    description = models.TextField()
    discount = models.FloatField()
    start_date = models.DateTimeField(default = datetime.now)
    end_date = models.DateTimeField(null = True)
    paused = models.BooleanField(default=False)
    def status(self):
        expired = self.end_date and self.end_date < datetime.now(timezone.utc)
        pending = self.start_date > datetime.now(timezone.utc)

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
    category = models.ForeignKey(Category, on_delete = models.PROTECT)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now_add = True)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 255)
    email = models.EmailField()

class Address(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)

    customer = models.ForeignKey(
        Customer, null=False, on_delete=models.CASCADE, related_name="addresses")
    is_shipping = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    street1 = models.CharField(max_length=100, null=True)
    apartment_no = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    country_code = models.CharField(max_length=3, null=True)

    
class Customer(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 255)
    email = models.EmailField()


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
    placed_at = models.DateTimeField(auto_now_add = True)
    customer = models.ForeignKey(Customer, on_Delete = models.PROTECT)

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, onDelete = models.PROTECT)
    order = models.ForeignKey(Order, onDelete = models.PROTECT)
    quantity= models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits= 6, decimal_places = 2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    id = models.UUIDField(default=uuid4, editable=False,
                          unique=True, primary_key=True)
    product = models.ForeignKey(Product, onDelete = models.CASCADE)
    cart = models.ForeignKey(Cart, onDelete = models.CASCADE)
    quantity= models.PositiveIntegerField()
 





    