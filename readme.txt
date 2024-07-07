1)Клонирование репозитория:

git clone https://github.com/Ldan1801/SummerPractice
cd SummerPractice

2.1)Создание и активация среды Conda:

conda env create -f environment.yml
conda activate image_app_env

ИЛИ

2.2)Создание и активация виртуального окружения:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3)Запуск приложения

python image_app.py