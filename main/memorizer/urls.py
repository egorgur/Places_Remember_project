from django.urls import path
from . import views

app_name="memorizer"

urlpatterns = [
    path("", views.redirect_to_main, name="redirect_to_main"),
    path("memories/", views.memories_menu_view, name="memories"),
    path("memories/create", views.create_memo_view, name="create_memo"),
    path("memories/<str:pk>", views.memo_view, name="view_memo"),
    path("memories/<str:pk>/delete", views.delete_memo, name="delete_memo")
]
