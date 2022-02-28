Для запуска Celery.
Первый териминал
1) cd /home - в терменале входим в папку где проект
2) cd ~/diplom-master - входим в сам проект
3) source venv/bin/activate - запускаем вертуальное окружение
4) celery -A имя_приложения worker -l info
Второй терминал
1) cd /home - в терменале входим в папку где проект
2) cd ~/diplom-master - входим в сам проект
3) source venv/bin/activate - запускаем вертуальное окружение
4) celery -A имя_приложения beat -l info