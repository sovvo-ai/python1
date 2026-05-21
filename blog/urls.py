from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api_views
from blog import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet, basename='api_category')
router.register(r'posts', api_views.PostViewSet, basename='api_post')
urlpatterns =[
    path('',views.post_list,name='post_list'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(
    template_name='registration/login.html',
    redirect_authenticated_user=True
), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
    next_page='post_list'
), name='logout'),
]