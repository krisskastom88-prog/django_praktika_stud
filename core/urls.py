# core/urls.py
# Изменения:
# - Добавлен путь dashboard/
# - Раскомментированы некоторые пути (можно будет включить позже)
# - Добавлены пути для добавления сущностей (пока закомментированы)

from django.urls import path
from . import views

urlpatterns = [
    
    # Главная страница (вход + регистрация)
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Авторизация и выход
    path('logout/', views.logout_view, name='logout'),

    # Дашборды по ролям
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Списки (раскомментировать, когда будут вьюхи)
    # path('students/', views.students_list, name='students_list'),
    # path('companies/', views.companies_list, name='companies_list'),
    # path('practices/', views.practices_list, name='practices_list'),
    # path('reports/', views.reports_list, name='reports_list'),

    # Добавление сущностей (раскомментировать позже)
    # path('students/add/', views.add_student, name='add_student'),
    # path('companies/add/', views.add_company, name='add_company'),
    # path('practices/add/', views.add_practice, name='add_practice'),
]