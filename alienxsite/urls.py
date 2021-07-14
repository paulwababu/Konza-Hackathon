from django.urls import path, include
from alienxsite import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prometheus/', views.prometheus, name='prometheus'),
    path('404/', views.notfound, name="404"),
    path('client/', views.client, name="client"),
    path('scanner/', views.scanner, name="scanner"),
    path('pentest/', views.pentest, name="pentest"),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('helloworld/', views.HelloWorldView.as_view(), name='hello'),
]