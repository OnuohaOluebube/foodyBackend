from django.urls import path,include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders',views.OrderViewSet, basename='orders')
products_router  = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')
carts_router  = routers.NestedDefaultRouter(router, 'carts', lookup = 'cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls))
   
   
]
