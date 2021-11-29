"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from magazine.views import Login, Logout, Register, ProductCreateView, ProductDeleteView, ProductListView, \
    ProductUpdateView, ProductBuyView, ProductListBuyView, OrderReturnCreateView, OrderListView, OrderAdmin, \
    ReturnUserConfirm, ReturnUserDelete

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('product/buy/', ProductBuyView.as_view(), name='product-buy'),
    path('product/', ProductListBuyView.as_view(), name='product'),
    path('order/return/', OrderReturnCreateView.as_view(), name='order-return'),
    path('order/', OrderListView.as_view(), name='order'),
    path('order-admin/', OrderAdmin.as_view(), name='order-admin'),
    path('order-admin/confirm', ReturnUserConfirm.as_view(), name='order-return-confirm'),
    path('order-admin/delete', ReturnUserDelete.as_view(), name='order-return-delete'),

]



