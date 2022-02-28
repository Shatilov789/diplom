Сначала запустите Django и Redis.
Для запуска Celery.

Первый териминал:
- cd /home - в терменале входим в папку где проект
- cd ~/diplom-master - входим в сам проект
- source venv/bin/activate - запускаем вертуальное окружение
- celery -A имя_приложения worker -l info
- 
Второй терминал:
- cd /home - в терменале входим в папку где проект
- cd ~/diplom-master - входим в сам проект
- source venv/bin/activate - запускаем вертуальное окружение
- celery -A имя_приложения beat -l info

Инструкция с настройкой и запускам по шагам: https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
