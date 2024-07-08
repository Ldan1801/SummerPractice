# Инструкция для запуска

### 1)Клонирование репозитория:

git clone https://github.com/Ldan1801/SummerPractice

cd SummerPractice

### 2.1)Создание и активация среды Conda:

conda env create -f environment.yml

conda activate image_app_env

### ИЛИ

### 2.2)Создание и активация виртуального окружения:

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

### 3)Запуск приложения

python image_app.py

## Возможные ошибки:

1)Имя "conda" не распознано как имя командлета, функции, файла сценария или выполняемой программы. Проверьте прав
ильность написания имени, а также наличие и правильность пути, после чего повторите попытку.

*Решение:*
1. Убедитесь, что Anaconda установлена
2. Добавьте Anaconda в PATH:
  * Откройте "Параметры системы" -> "Переменные среды".
  * Найдите переменную Path в разделе "Системные переменные" и выберите "Изменить".
  * Добавьте путь к папке Scripts Anaconda или Miniconda (например, C:\Users\ВашеИмя\Anaconda3\Scripts или C:\Users\ВашеИмя\Miniconda3\Scripts).
  * Сохраните изменения и перезагрузите командную строку.
