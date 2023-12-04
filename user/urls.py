from django.urls import path

from . import views

urlpatterns = [
    path('', views.manageUser, name="manageuser"),
    path('tambah-user/', views.tambahUser, name="tambah-user"),
    path('update-user/', views.updateUser, name="update-user"),
    path('delete-user/', views.deleteUser, name="delete-user"),
]
