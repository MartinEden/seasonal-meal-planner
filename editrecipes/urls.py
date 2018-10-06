from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<str:name>/', views.recipe, name='recipe'),
    path('month/<int:month_id>/', views.month),
    path('month', views.month),
    path('category/<str:category>/', views.category, name='category'),
    path('category', views.category),
    path('sidedish/<str:sidedish>/<int:month_id>/', views.sidedish,
         name='sidedish'),
    path('sidedish/<str:sidedish>/', views.sidedish, name='sidedish'),
    path('sidedish', views.sidedish),
    path('select-recipes/<int:month_id>/', views.select_recipes),
    path('select-recipes', views.select_recipes),
    path('shopping-list', views.shopping_list, name='shopping_list'),
    path('search', views.search, name='search'),
    path('search/<str:ingredient>/', views.search, name='search'),
    path('ingredients', views.ingredients)
]