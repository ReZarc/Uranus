from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:post_id>', views.comment, name='comment')
]