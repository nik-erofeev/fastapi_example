# Используем базовый образ Python с установленным uvicorn
FROM python:3.11-slim

# Устанавливаем переменную среды для указания Python не создавать файлы pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем переменную среды для указания Python выводить вывод без буферизации
ENV PYTHONUNBUFFERED 1

# Создаем и устанавливаем рабочую директорию /app
RUN mkdir /app
WORKDIR /app

# Копируем зависимости файла зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущей директории в контейнер в директорию /app
COPY . /app/

# Команда для запуска приложения FastAPI через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]