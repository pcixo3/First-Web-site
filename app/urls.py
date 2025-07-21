from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.detail_view, name='detail'),
    path('car_create/', views.car_create, name='car_create'),
    path('car/<int:car_id>/update/', views.car_update, name='car_update'),
    path('car/<int:car_id>/delete/', views.car_delete, name='car_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
