
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.userLogout, name='logout'),
    path('home/', views.BlogListView.as_view(), name='blog_list'),
    path('home/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('comment/like/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('home/tag/<slug:slug>/', views.tagged, name='tagged'),
]
