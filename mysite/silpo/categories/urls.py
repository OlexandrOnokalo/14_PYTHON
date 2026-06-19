from django.urls import path

from categories import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='list'),
    path('create/', views.category_create, name='create'),
    path('edit/<int:category_id>/', views.category_edit, name='edit'),
    path('delete/<int:category_id>/', views.category_delete, name='delete')
]