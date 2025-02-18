from django.urls import path

from . import views

app_name = "pantry"
urlpatterns = [
    path("", views.index, name="index"),
    path("food_substitutes/search", views.search_food_substitutes, name="search_food_substitutes"),
    path("ingredients", views.ingredients, name="ingredients"),
    path("ingredients/<int:ingredient_id>/", views.show_ingredient, name="show_ingredient"),
    path("ingredients/delete", views.delete_ingredient, name="delete_ingredient"),

    path("items/", views.food_items, name="food_items"),
    path("items/<int:item_id>/", views.show_food_item, name="show_food_item"),
]