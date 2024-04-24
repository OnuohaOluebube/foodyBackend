from django.db import transaction
from rest_framework import serializers
from . import models


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Collection
        fields = ['id', 'title', 'product_count', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'unit_price', 'description','quantity', 'collection','review_count']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'description', 'name']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return models.Review.objects.create(product_id = product_id, **validated_data)
    

class CartItemSerialiizer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,obj:models.CartItem):
        return obj.quantity * obj.product.unit_price

    class Meta:
        model = models.CartItem
        fields = ['id','product','quantity', 'total_price']

    

class AddCartItemSerialiizer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    class Meta:
        model = models.CartItem
        fields = ['id','quantity', 'product_id']

    def validate_product_id(self, value):
        if not models.Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No product with the given ID found')
        return value
        
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = models.CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except models.CartItem.DoesNotExist:
            self.instance = models.CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']

class CartSerialiizer(serializers.ModelSerializer):
    items = CartItemSerialiizer(many=True, read_only = True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self,obj:models.Cart):
        
        return (sum([(item.quantity * item.product.unit_price) for item in obj.items.all()]))

    class Meta:
        model = models.Cart
        fields = ['id','items', 'total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Customer
        fields = ['id', 'user_id', 'phone', 'birth_day']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity','unit_price']
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = models.Order
        fields = ['id', 'customer', 'items', 'payment_status','created_at']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not models.Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')
        if models.CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id
        

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            

            cart_items = models.CartItem.objects.select_related('product').filter(cart_id = cart_id)
            customer= models.Customer.objects.get(user_id = user_id)
            order = models.Order.objects.create(customer = customer)
            order_items = [
                models.OrderItem(
                    product = item.product,
                    quantity = item.quantity, 
                    unit_price = item.product.unit_price, 
                    order = order
                ) for item in cart_items]
            models.OrderItem.objects.bulk_create(order_items)
            models.Cart.objects.filter(pk = cart_id).delete()
            return order
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['payment_status']
    





