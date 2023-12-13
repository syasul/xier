from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('pesanan-keranjang/<int:pesanan_id>/', views.pesanKeranjang, name="pesanKeranjang"),
    path('pesanan-user/<int:pembeli_id>/', views.pesananUser, name="pesananUser"),
    path('pesanan-admin/', views.pesananAdmin, name="pesananAdmin")
    
]