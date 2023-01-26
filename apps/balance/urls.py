from django.urls import path

from apps.balance import views

urlpatterns = [
    path('payed/', views.SuccessPayViewSet.as_view({"post": "post"})),
    path('balance/', views.BalanceViewSet.as_view({"get": "get"}))
]
