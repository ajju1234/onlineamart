"""Ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from shopping.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    url(r'^update_item/$', update_item_quantity, name='update_item_quantity'),
    url(r'^thank_you/$', thank_you, name="thank_you"),
    url(r'^confirm_order/$', confirm_order, name="confirm_order"),
    url(r'^remove_item/$', remove_item, name="remove_item"),
    url(r'^cart/$', cart, name="cart"),
    url(r'^credit_card_page/$', credit_card_page, name="credit_card"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('product_details/<int:product_id>/', product_details, name="product_details"),
    path('add_review/<int:product_id>/', add_review, name="add_review"),
    path('user_login', user_login, name = "user_login"),
    path('user_registration', user_registration, name="user_registration"),
    path('user_logout', user_logout, name = 'user_logout'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)