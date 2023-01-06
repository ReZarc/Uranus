from django.urls import path 
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('release/', views.post_release, name='post_release'),
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('comment_delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('my_post/', views.my_post_list, name='my_post'),
    path('favorite_add/<int:post_id>/', views.favorite_add, name='favorite_add'),
    path('favorite_del/<int:post_id>/', views.favorite_del, name='favorite_del'),
    path('my_favorite/', views.my_favorite, name='my_favorite'),
    path('post_list/<int:user_id>/', views.post_list, name='post_list'),
]
