from django.urls import path

from apps.subdomains import views

urlpatterns = [
    path('subdomain/', views.SubdomainController.as_view({"get": "list", "post": "create"})),
    path('subdomain/check/', views.SubdomainController.as_view({"get": "check_exists"})),
    path('subdomain/check/premium', views.SubdomainController.as_view({"get": "get_premium_settings"})),
    path('subdomain/<int:pk>/', views.SubdomainController.as_view({"get": "get_subdomain"}))
]
