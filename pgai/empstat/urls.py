# ml_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ml-features/', views.ml_features, name='ml_features'),
    path('data_analysis/', views.data_analysis, name='data_analysis'), 
    path('timeseries_analysis/', views.timeseries_analysis, name='timeseries_analysis'), 
    path('sales_analysis/', views.sales_analysis, name='sales_analysis'),
    path('model_list/', views.model_list, name='model_list'),
    path('model_details/<str:model_name>/', views.model_details, name='model_details'),
    path('data_analysis/<str:model_name>/', views.data_analysis_model, name='data_analysis_model'),

    
    
]
