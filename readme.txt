1)Клонирование репозитория:

git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd <ИМЯ_РЕПОЗИТОРИЯ>
Создание и активация среды Conda:

2.1)Создание и активация среды Conda:

conda env create -f environment.yml
conda activate image_app_env
Запуск приложения:

ИЛИ

2.2)Создание и активация виртуального окружения:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3)Запуск приложения
python image_app.py