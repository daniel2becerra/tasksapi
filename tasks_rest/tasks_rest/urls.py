from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path('users/',include('users.urls')),
    path('tasks/',include('tasks.urls')),
]
