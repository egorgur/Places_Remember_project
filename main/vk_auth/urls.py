from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="vk_auth"

urlpatterns = [
    path("", views.auth_view, name="auth_view"),
    path("process/", views.auth_processor, name="auth_processor"),
    path("logout/", views.leave_account, name="leave_account")
]
