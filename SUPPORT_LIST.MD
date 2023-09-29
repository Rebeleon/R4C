Установить зависимости по requirements.txt
В settings прописать значения EMAIL_HOST_USER и EMAIL_HOST_PASSWORD. Настроить gmail для отправки почты.

При использовании development server:
task 1: POST запрос на http://127.0.0.1:8000/api/create_robot/
task 2: Запрос на http://127.0.0.1:8000/api/download-summary/