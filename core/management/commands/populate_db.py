# core/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Student, Company, Practice
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        # Удаляем старые данные (опционально)
        # self.stdout.write('Удаление старых данных...')
        # Student.objects.all().delete()
        # Company.objects.all().delete()
        # Practice.objects.all().delete()
        # User.objects.filter(role='student').delete() # Не удаляем админов/преподов

        self.stdout.write('Создание пользователей-студентов и профилей...')

        # Списки для генерации данных
        first_names = ['Александр', 'Михаил', 'Дмитрий', 'Иван', 'Сергей', 'Андрей', 'Алексей', 'Максим', 'Евгений', 'Денис',
                       'Анастасия', 'Мария', 'Екатерина', 'Дарья', 'Анна', 'Ольга', 'Татьяна', 'Наталья', 'Ирина', 'Светлана']
        last_names = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Волков', 'Смирнов', 'Попов', 'Лебедев', 'Новиков', 'Морозов',
                      'Соколова', 'Волкова', 'Петрова', 'Смирнова', 'Кузнецова', 'Иванова', 'Попова', 'Лебедева', 'Новикова', 'Морозова']
        groups = [f'ИУ-{i}{j}' for i in range(1, 7) for j in ['А', 'Б', 'В']] # Пример: ИУ-1А, ИУ-1Б, ...
        companies_data = [
            {'name': 'АО "Технократ"', 'address': 'г. Москва, ул. Программистов, д. 1'},
            {'name': 'ООО "Кодекс"', 'address': 'г. Санкт-Петербург, пр. Логики, д. 42'},
            {'name': 'ОАО "БитСофт"', 'address': 'г. Новосибирск, пр. Алгоритмов, д. 10'},
            {'name': 'ЗАО "ДигиКорп"', 'address': 'г. Екатеринбург, ул. Сигналов, д. 7'},
            {'name': 'ООО "ВебЛайн"', 'address': 'г. Казань, пр. Интернета, д. 25'},
        ]

        # Создаём студентов
        created_users = []
        for i in range(20):
            username = f'student{i+1:02d}'
            email = f'{username}@university.edu'
            password = 'password123' # Не безопасно для продакшена!

            # Проверим, существует ли пользователь
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'role': 'student'
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  Создан пользователь {username}')
            else:
                self.stdout.write(f'  Пользователь {username} уже существует')

            # Проверим, существует ли профиль студента
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f'{last_names[i]} {first_names[i]}',
                    'group_number': random.choice(groups),
                    'email': email
                }
            )
            if created:
                self.stdout.write(f'    Создан профиль студента для {username}')
            else:
                self.stdout.write(f'    Профиль студента для {username} уже существует')

            created_users.append(user)

        self.stdout.write('Создание предприятий...')
        created_companies = []
        for comp_data in companies_data:
            company, created = Company.objects.get_or_create(
                name=comp_data['name'],
                defaults={
                    'address': comp_data['address']
                }
            )
            if created:
                self.stdout.write(f'  Создано предприятие {comp_data["name"]}')
            else:
                self.stdout.write(f'  Предприятие {comp_data["name"]} уже существует')
            created_companies.append(company)

        self.stdout.write('Создание практик...')
        practice_descriptions = [
            "Прохождение практики на базе предприятия.",
            "Ознакомление с производственным процессом.",
            "Разработка программного обеспечения.",
            "Анализ бизнес-процессов.",
            "Работа в команде разработчиков."
        ]

        for user in created_users:
            # Получаем профиль студента
            student_profile = Student.objects.get(user=user)
            # Выбираем случайное предприятие
            company = random.choice(created_companies)
            # Генерируем даты
            start_date = date.today() - timedelta(days=random.randint(30, 180))
            end_date = start_date + timedelta(days=random.randint(30, 90))
            # Выбираем описание
            description = random.choice(practice_descriptions)

            # Создаём практику
            practice, created = Practice.objects.get_or_create(
                student=student_profile,
                company=company,
                defaults={
                    'start_date': start_date,
                    'end_date': end_date,
                    'description': description
                }
            )
            if created:
                self.stdout.write(f'    Создана практика для {student_profile.full_name} на {company.name}')
            else:
                self.stdout.write(f'    Практика для {student_profile.full_name} на {company.name} уже существует')

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )