# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница (вход + регистрация)
    path('', views.home, name='home'),

    # Авторизация и выход
    path('logout/', views.logout_view, name='logout'),

    # Дашборды по ролям
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Списки — пока закомментированы, потому что вьюх нет
    # path('students/', views.students_list, name='students_list'),
    # path('companies/', views.companies_list, name='companies_list'),
    # path('practices/', views.practices_list, name='practices_list'),
    # path('reports/', views.reports_list, name='reports_list'),

    # Добавление сущностей — тоже пока нет вьюх
    # path('students/add/', views.add_student, name='add_student'),
    # path('companies/add/', views.add_company, name='add_company'),
]