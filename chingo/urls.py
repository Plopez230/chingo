from django.urls import path

from . import views

app_name = 'chingo'

urlpatterns = [
	path('list/<int:list_id>/', views.list_view, name='list'),
	path('list/<int:list_id>/edit/', views.list_edit_view, name='list_edit'),
	path('list/<int:list_id>/edit_word/', views.word_edit_view, name='word_edit'),
	path('list/<int:list_id>/add/<int:word_id>/', views.word_add_from_database_view, name='word_add_from_db'),
	path('list/<int:list_id>/remove/<int:word_id>/', views.word_remove_view, name='word_remove'),
	path('list/<int:list_id>/add/', views.word_add_view, name='word_add'),
	path('list/add/', views.list_add_view, name='list_add'),
	path('search/', views.search_view, name='search'),
	path('suggest/', views.word_suggest_view, name='word_suggest'),
	path('test/', views.test_view, name='test'),
	path('check_test/', views.test_check_view, name='test_check'),
	path('', views.index_view, name='index'),
]
