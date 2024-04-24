from django.db.models import Count
from rest_framework import viewsets, mixins, decorators
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from . import models, serializers
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission



# Create your views here.

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = models.Collection.objects.annotate(product_count = Count('products__id')).all()
    serializer_class = serializers.CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        collection = models.Collection.objects.filter(pk = kwargs['pk'])
        print("collection", (collection).values_list())
        # if collection.products.count() == 0:
        #         return Response({'error': 'Cannot delete collection with a product'})
        return super().destroy(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.annotate(review_count = Count('review__id')).all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}
 
class CartViewSet(mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = models.Cart.objects.prefetch_related('items__product').all()
    serializer_class = serializers.CartSerialiizer

    

class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerialiizer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerialiizer
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet( viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [IsAdminUser]

    @decorators.action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')


    @decorators.action(detail=False, methods=('GET', 'PUT'), permission_classes=[IsAuthenticated])
    def me(self, request):
        customer= models.Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        
class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['patch','get', 'delete', 'options','head']

    def get_permissions(self):
        if  self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateOrderSerializer(data = self.request.data, context = {"user_id" : self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
        

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Order.objects.all()
        customer_id = models.Customer.objects.only('id').get(user_id = user.id)
        return models.Order.objects.filter(customer = customer_id)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateOrderSerializer
        return serializers.OrderSerializer
    

    



