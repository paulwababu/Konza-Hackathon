from django.urls import path, include
from carwash import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('reports/', views.reports, name='reports'),
    path('hom/', views.hom, name='hom'),
    path('home2/', views.home2, name='home2'),
    path('logout/', views.logout, name='logout'),
]