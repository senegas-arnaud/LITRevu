"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'), 
    path('ticket_create/', views.ticket_create_view, name='ticket_create'),
    path('ticket_edit/<int:pk>/', views.ticket_edit_view, name='ticket_edit'),
    path('ticket_delete/<int:pk>/', views.ticket_delete_view, name='ticket_delete'),
    path('review_create/', views.review_create_view, name='review_create'), 
    path('review_edit/<int:pk>/', views.review_edit_view, name='review_edit'),
    path('review_delete/<int:pk>/', views.review_delete_view, name='review_delete'), 
    path('review_answer/', views.review_answer_view, name='review_answer'),
    path('my_post_ticket/', views.my_post_ticket_view, name='my_post_ticket'),  
    path('my_post_review/', views.my_post_review_view, name='my_post_review'),  
    path('follow/', views.follow_view, name='follow'), 
]
