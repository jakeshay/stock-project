from django.urls import path
from . import models
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mystocks/', views.myStocks, name='myStocks'),
    path('addstocks/', views.addStocks, name='addStocks'),
    path('<str:symbol>/delete/', views.deleteStocks, name='deleteStocks'),
    path('analysis/', views.analysis, name='analysis'),
    path('<str:symbol>/', views.detail, name='detail'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
]
 
