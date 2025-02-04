from django.urls import path
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views

app_name = 'social'
urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('user/edit/', views.edit_user, name='edit_user'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('ticket/', views.ticket, name='ticket'),
    path('posts/create_post/', views.create_post, name='create_post'),
    path('posts/', views.post_list, name='list'),
    path('posts/post/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('posts/<int:post_id>/comment/', views.post_comment, name='comments'),
    path('posts/detail/<int:pk>/', views.post_detail, name='detail'),
    path('posts/edit_post/<post_id>/', views.edit_post, name='edit_post'),
    path('posts/delete_post/<post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.post_search, name='search'),
    path('like_post/', views.like_post, name='like_post'),


]