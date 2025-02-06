from django.urls import path

from . import views

app_name = "pantry"
urlpatterns = [
    path("", views.index, name="index"),
    path("items/", views.all_items, name="all_items"),
    path("<int:item_id>/", views.detail, name="detail"),
    path("items/new", views.new_item, name="new_item"),
]