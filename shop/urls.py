from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListApiView.as_view()),
    path('products/<int:pk>/', views.ProductDetailApiView.as_view()),
    path('categories/', views.CategoryApiView.as_view()),
    path('choosen/', views.ChoosenListApiView.as_view()),
    path('<int:pk>/choosen/add/', views.ChoosenAdd.as_view()),
    path('<int:pk>/choosen/delete/', views.ChoosenDelete.as_view()),
]