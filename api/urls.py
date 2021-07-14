from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('carwash/', views.ListCarsWashed.as_view()),
    path('carwash/<int:pk>/', views.DetailCarsWashed.as_view()),

    path('mgmt/', views.ListStocks.as_view()),
    path('mgmt/<int:pk>/', views.DetailStocks.as_view()),
    path('rest-auth/', include('rest_auth.urls')),

    path('contacts/', views.ContactView.as_view(), name='contacts'),

    path("todo",views.ListTodoAPIView.as_view(),name="todo_list"),
    path("todo/create/", views.CreateTodoAPIView.as_view(),name="todo_create"),
    path("todo/update/<int:pk>/",views.UpdateTodoAPIView.as_view(),name="update_todo"),
    path("todo/delete/<int:pk>/",views.DeleteTodoAPIView.as_view(),name="delete_todo"),

    path('docs/', include_docs_urls(title='Prometheus')),
]