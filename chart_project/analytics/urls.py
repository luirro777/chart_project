from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/sales-by-category/', views.SalesDataView.as_view(), name='sales-api'),
    path('trend/', views.SalesTrendView.as_view(), name='trend'),
]