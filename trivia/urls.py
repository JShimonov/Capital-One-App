from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='trivia-home'),
    path('categories/', views.categories, name='trivia-categories'),
    path('listcategory/<id>', views.listcategory, name='trivia-listcategory'),
    path('airdate/<id>', views.airdatetrivia, name='trivia-airdate'),
    path('difficulty/<id>', views.difficultytrivia, name='trivia-difficulty'),
    path('results/', views.results_trivia, name='trivia-results'),
]
