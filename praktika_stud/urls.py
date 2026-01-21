# praktika_stud/urls.py

from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # Главная страница (вход/регистрация)
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'), # Студент
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'), # Преподаватель
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), # Админ
    path('logout/', views.logout_view, name='logout'), # Выход
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)