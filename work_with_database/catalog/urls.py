from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.phone_detail, name='phone_detail'),
]