# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Student, Company, Practice, Report
import json

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_supervisor(user):
    return user.is_authenticated and user.role in ['admin', 'supervisor']

def is_student(user):
    return user.is_authenticated and user.role in ['admin', 'student']

# --- Основные страницы ---
def home(request):
    # Если пользователь уже авторизован, перенаправляем его на страницу, соответствующую его роли
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'supervisor':
            return redirect('supervisor_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
        else:
            # Если роль неизвестна, отправим на общую панель (или на главную)
            return redirect('dashboard')

    # Если не авторизован, показываем страницу входа/регистрации
    if request.method == 'POST':
        # Определим, какая форма была отправлена
        if 'login_username' in request.POST:
            # Это вход
            username = request.POST['login_username']
            password = request.POST['login_password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # После входа снова проверим роль и перенаправим
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'supervisor':
                    return redirect('supervisor_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        elif 'register_email' in request.POST:
            # Это регистрация
            email = request.POST['register_email']
            password1 = request.POST['register_password1']
            password2 = request.POST['register_password2']
            username = request.POST['register_username']
            role = request.POST.get('register_role', 'student')

            if password1 != password2:
                messages.error(request, 'Пароли не совпадают.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password1, role=role)
                    # Если роль - student, можно создать связанную модель Student
                    if role == 'student':
                         # !!! ВАЖНО: Тут нужно решить, как связывать Student и User
                         # Вариант 1: Если у Student есть поле user = models.OneToOneField(User, ...)
                         student = Student.objects.create(user=user, full_name=username) # <<< ПРИМЕР >>>
                    login(request, user)
                    messages.success(request, 'Регистрация успешна! Добро пожаловать!')
                    # После регистрации тоже проверим роль и перенаправим
                    if user.role == 'admin':
                        return redirect('admin_dashboard')
                    elif user.role == 'supervisor':
                        return redirect('supervisor_dashboard')
                    elif user.role == 'student':
                        return redirect('student_dashboard')
                    else:
                        return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Ошибка при регистрации: {str(e)}')

    return render(request, 'core/login_register.html')

# --- Страницы для разных ролей ---
@login_required
def student_dashboard(request):
    # Логика для студента
    # Проверим, является ли пользователь студентом
    if request.user.role != 'student':
        # Если нет, перенаправим или покажем ошибку
        # Пока просто перенаправлю на главную
        return redirect('home')

    # Получаем профиль студента, связанный с пользователем
    try:
        user_student = request.user.student # <<< ИСПОЛЬЗУЕМ related_name ИЗ МОДЕЛИ >>>
    except Student.DoesNotExist:
        # Если профиль не найден, можно создать его или показать ошибку
        # Пока просто покажем пустой список
        user_student = None
        practices = Practice.objects.none()
    else:
        # Получаем все практики, связанные с этим студентом
        practices = Practice.objects.filter(student=user_student).select_related('company') # <<< select_related для эффективности >>>

    context = {
        'student_profile': user_student, # Передаём профиль студента
        'practices': practices, # Передаём его практики
    }
    return render(request, 'core/student_dashboard.html', context)

@login_required
def supervisor_dashboard(request): # <<< ЭТА СТРОКА ДОЛЖНА БЫТЬ С ОТСТУПОМ ТАКИМ ЖЕ, КАК И ДРУГИЕ ФУНКЦИИ НА ЭТОМ УРОВНЕ >>>
    # Логика для преподавателя
    # Например, показать студентов, закреплённых за ним (если такое поле есть)
    # Или все практики
    practices = Practice.objects.all() # <<< ПРИМЕР >>>
    context = {
        'practices': practices,
    }
    return render(request, 'core/supervisor_dashboard.html', context)

@login_required
def admin_dashboard(request): # <<< ЭТА СТРОКА ТОЖЕ >>>
    # Логика для администратора
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    active_practices = Practice.objects.filter(status='ongoing').count()
    total_reports = Report.objects.count()

    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'active_practices': active_practices,
        'total_reports': total_reports,
    }
    return render(request, 'core/admin_dashboard.html', context)

# --- Страница выхода ---
def logout_view(request):
    logout(request)
    return redirect('home') # Перенаправить на главную после выхода