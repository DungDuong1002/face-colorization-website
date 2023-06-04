from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('my_image_conversion', views.MyImageAPI)

urlpatterns = [
    path('', views.home, name='home'),
    path('result', views.display_image, name='result'),
    # path('upload', views.upload_image, name='image_upload'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='image/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('colorize/', views.upload_image, name='upload_image'),
    # path('api/image_conversion/', views.ImageConversionAPI.as_view(), name='image_conversion_api'),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)