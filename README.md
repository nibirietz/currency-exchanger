# currency-exchanger

REST-API для обмена валют на Python.

Проект реализован по ТЗ
из [роадмапы Сергея Жукова](https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/).
Реализован на Python(3.14) без применения фреймворков.

##### Функционал проекта:

- добавление валют;
- создание курсов валют;
- вычисление перевода из одной валюты в другой.

---

#### Установка

##### Вручную:

Требуется Python(3.14+).

```bash
git clone https://github.com/nibirietz/currency-exchanger.git
cd currency-exchanger

# Предварительно можете поставить и активировать виртуальное окружение
# (способ для Linux):
# python -m venv .venv
# source .venv/bin/activate

pip install -r requirements.txt
# Запуск:
python main.py
```

##### Через Docker:

```bash
git clone https://github.com/nibirietz/currency-exchanger.git
cd currency-exchanger
docker build -t currency-exchanger .
# Запуск:
chmod +x run.sh
./run.sh
```

##### Фронтенд:

```bash
git clone https://github.com/zhukovsd/currency-exchange-frontend.git
cd currency-exchange-frontend
# Запустите скрипт, предварительно сделав его запускаемым(для Linux):
chmod +x launch-local-nginx.sh
./launch-local-nginx.sh
```
