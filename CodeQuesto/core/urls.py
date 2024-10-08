# core/urls.py
# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('welcome/', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),  # New course list URL
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('module/', views.module, name='module'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('coding_exercise/', views.coding_exercise, name='coding_exercise'),
    path('submit_code/', views.submit_code, name='submit_code'),  
    # Add more URLs as needed
]
