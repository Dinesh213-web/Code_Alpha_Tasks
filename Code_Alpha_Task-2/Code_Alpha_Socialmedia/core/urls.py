from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Feed
    path('', views.feed_view, name='feed'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Posts
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),

    # Comments
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),

    # Likes
    path('post/<int:post_id>/like/', views.toggle_like_view, name='toggle_like'),

    # Follow
    path('user/<str:username>/follow/', views.toggle_follow_view, name='toggle_follow'),

    # Explore
    path('explore/', views.explore_view, name='explore'),
]
