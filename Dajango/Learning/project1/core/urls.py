from django.urls import path
from .views import hello , templateshome,create_product,get_products ,update_product,delete_product

urlpatterns = [
    path("hello/", hello),
    path("templateshome/", templateshome),
    path("create_product/", create_product),
    path("get_product/", get_products),
    path("update_product/", update_product),
    path("delete_product/", delete_product),
]