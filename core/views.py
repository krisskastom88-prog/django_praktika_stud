# core/views.py
# Изменения:
# - Добавлена поддержка выбора роли при регистрации
# - Добавлена вьюха dashboard (единая для всех, с редиректом по роли)
# - Улучшена фильтрация в supervisor_dashboard (только свои практики)
# - Добавлена базовая обработка ошибок

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Student, Company, Practice, Report

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        # Временно возвращаем простой текст вместо редиректа
        return render(request, 'core/base.html', {'message': 'Вы авторизованы, но редирект отключён для теста'})

    if request.method == 'POST':
        if 'login_username' in request.POST:
            # Вход
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')

        elif 'register_username' in request.POST:
            # Регистрация
            username = request.POST.get('register_username')
            email = request.POST.get('register_email', '')
            password1 = request.POST.get('register_password1')
            password2 = request.POST.get('register_password2')
            role = request.POST.get('register_role', 'student')

            if password1 != password2:
                messages.error(request, 'Пароли не совпадают.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Такое имя пользователя уже занято.')
            else:
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                        role=role
                    )
                    if role == 'student':
                        Student.objects.create(
                            user=user,
                            full_name=username,
                            group_number='Не указана',
                        )
                    login(request, user)
                    messages.success(request, 'Регистрация успешна! Добро пожаловать!')
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Ошибка регистрации: {str(e)}')

    return render(request, 'core/login_register.html')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.warning(request, 'Доступ запрещён для вашей роли.')
        return redirect('dashboard')

    student = request.user.student_profile  # используем related_name
    practices = Practice.objects.filter(student=student)\
                                .select_related('company', 'supervisor')\
                                .prefetch_related('reports')\
                                .order_by('-start_date')

    context = {
        'student': student,
        'practices': practices,
    }
    return render(request, 'core/student_dashboard.html', context)


@login_required
def supervisor_dashboard(request):
    if request.user.role not in ['supervisor', 'admin']:
        messages.warning(request, 'Доступ запрещён.')
        return redirect('dashboard')

    practices = Practice.objects.filter(supervisor=request.user)\
                                .select_related('student', 'company')\
                                .prefetch_related('reports')\
                                .order_by('-start_date')

    context = {
        'practices': practices,
    }
    return render(request, 'core/supervisor_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.warning(request, 'Доступ запрещён.')
        return redirect('dashboard')

    context = {
        'total_students': Student.objects.count(),
        'total_companies': Company.objects.count(),
        'active_practices': Practice.objects.filter(status='ongoing').count(),
        'total_reports': Report.objects.count(),
    }
    return render(request, 'core/admin_dashboard.html', context)



def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def dashboard(request):
    """
    Единый дашборд — перенаправляет пользователя на соответствующий дашборд в зависимости от роли.
    """
    if request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'supervisor':
        return redirect('supervisor_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        messages.warning(request, 'Неизвестная роль пользователя.')
        return redirect('home')