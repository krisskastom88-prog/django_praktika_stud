# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Student, Company, Practice, Report

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'supervisor':
            return redirect('supervisor_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('home')  # fallback

    if request.method == 'POST':
        if 'login_username' in request.POST:
            # Вход
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'supervisor':
                    return redirect('supervisor_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')

        elif 'register_username' in request.POST:
            # Регистрация
            username = request.POST.get('register_username')
            email = request.POST.get('register_email', '')
            password1 = request.POST.get('register_password1')
            password2 = request.POST.get('register_password2')

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
                        role='student'  # всегда студент при самостоятельной регистрации
                    )
                    # Создаём профиль студента
                    Student.objects.create(
                        user=user,
                        full_name=username,  # потом можно редактировать в профиле
                        group_number='Не указана',  # можно добавить поле в форму позже
                    )
                    login(request, user)
                    messages.success(request, 'Регистрация успешна! Добро пожаловать!')
                    return redirect('student_dashboard')
                except Exception as e:
                    messages.error(request, f'Ошибка регистрации: {str(e)}')

    return render(request, 'core/login_register.html')


# core/views.py  — обнови только функцию student_dashboard (остальное оставь как есть)

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.warning(request, 'Доступ запрещён для вашей роли.')
        return redirect('home')

    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = Student.objects.create(
            user=request.user,
            full_name=request.user.get_full_name() or request.user.username,
        )
    
    practices = Practice.objects.filter(student=student)\
        .select_related('company')\
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
        return redirect('home')

    # Пока показываем все практики — потом можно фильтровать по куратору
    practices = Practice.objects.select_related('student', 'company')\
                                .order_by('-start_date')

    context = {
        'practices': practices,
    }
    return render(request, 'core/supervisor_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.warning(request, 'Доступ запрещён.')
        return redirect('home')

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