# ml_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('ml-features/', views.ml_features, name='ml_features'),
    path('data_analysis/', views.data_analysis, name='data_analysis'), 
    path('timeseries_analysis/', views.timeseries_analysis, name='timeseries_analysis'), 
    path('sales_analysis/', views.sales_analysis, name='sales_analysis'),
    
    
]
