from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:subdomain>/api/v1/', include("apps.authorization.urls")),
    path('api/v1/', include("apps.authorization.urls")),
    path('api/v1/', include("apps.balance.urls")),
    path('api/v1/', include("apps.subdomains.urls"))
]
