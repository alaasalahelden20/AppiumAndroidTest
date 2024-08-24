from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(''         , views.app_list, name='app_list'),
    path('register/', views.register, name='register'),
    path('login/'   , auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/'  , auth_views.LogoutView.as_view(), name='logout'),

    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    path('app/new/', views.app_create, name='app_create'),
    path('app/<int:app_id>/edit/', views.app_update, name='app_update'),
    path('app/<int:app_id>/delete/', views.app_delete, name='app_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
