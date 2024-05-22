from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.redirect_to_main, name="redirect_to_main"),
    path("memories/", views.memories_menu_view, name="collection"),
    path("memories/create", views.create_memo_view, name="create_collection_view"),
    path("memories/<str:pk>", views.memo_view, name="collection_view"),
]
