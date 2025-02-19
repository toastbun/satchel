from django.urls import path

from . import views

app_name = "pantry"
urlpatterns = [
    path("", views.index, name="index"),

    path("ingredients", views.ingredients, name="ingredients"),
    path("ingredients/<int:ingredient_id>/", views.show_ingredient, name="show_ingredient"),
    path("ingredients/search", views.search_ingredient_names, name="search_ingredient_names"),
    path("ingredients/add", views.add_ingredient, name="add_ingredient"),
    path("ingredients/delete", views.delete_ingredient, name="delete_ingredient"),

    path("food_items", views.food_items, name="food_items"),
    path("food_items/<int:item_id>/", views.show_food_item, name="show_food_item"),
    # path("food_items/search", views.search_food_items, name="search_food_items"),
    path("food_items/add", views.add_food_item, name="add_food_item"),
    # path("food_items/delete", views.delete_food_item, name="delete_food_item"),
]