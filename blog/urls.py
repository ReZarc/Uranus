from django.urls import path 
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    # path('release/', views.release, name='release')
]
