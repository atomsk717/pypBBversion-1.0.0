from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/<slug:slug>/', views.forum_detail, name='forum_detail'),
    path('forum/<slug:slug>/new/', views.create_topic, name='create_topic'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:pk>/lock/', views.toggle_lock, name='toggle_lock'),

    # Delete Topic
    path('topic/<int:pk>/delete/', views.confirm_delete_topic, name='confirm_delete_topic'),
    path('topic/<int:pk>/delete/confirm/', views.delete_topic, name='delete_topic'),

    # Delete Post
    path('post/<int:pk>/delete/', views.confirm_delete_post, name='confirm_delete_post'),
    path('post/<int:pk>/delete/confirm/', views.delete_post, name='delete_post'),
]