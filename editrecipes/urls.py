from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/<str:name>/', views.recipe, name='recipe'),
    path('month/<int:month_id>/', views.month),
    path('month', views.month),
    path('year-chart', views.year_chart, name='year_chart'),
    path('tag-chart', views.tag_chart, name='tag_chart'),
    path('category/<str:category>/', views.category, name='category'),
    path('category', views.category, name='all_categories'),
    path('sidedish/<str:sidedish>/<int:month_id>/', views.sidedish,
         name='sidedish'),
    path('sidedish/<str:sidedish>/', views.sidedish, name='sidedish'),
    path('sidedish', views.sidedish, name='all_sidedishes'),
    path('select-recipes/<int:month_id>/', views.select_recipes),
    path('select-recipes', views.select_recipes, name='select_recipes'),
    path('shopping-list', views.shopping_list, name='shopping_list'),
    path('search', views.search, name='search'),
    path('search/<str:ingredient>/', views.search, name='search'),
    path('ingredients', views.ingredients, name='ingredients'),
    path('sort-into-aisles', views.sort_into_aisles, name='sort_into_aisles'),
    path('sort-into-aisles/<str:aisle>', views.sort_into_aisles,
         name='sort_into_aisles')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
