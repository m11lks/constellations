# constellations

[Русский](#русский) | [English](#english)

## Русский

Веб-приложение, которое показывает, какое созвездие находится в зените для заданных даты, времени и координат.

Бэкенд написан на FastAPI, расчёты делает PyEphem. Фронтенд написан на NiceGUI.

### Что умеет

- Определяет созвездие в зените по дате, времени (UTC), широте и долготе.
- На главной странице показывает одно из небесных тел (Солнце, Луна, Марс, Венера, Юпитер, Сатурн, Уран, Нептун; тело меняется каждый час) и созвездие, в котором оно сейчас находится.
- Ищет статьи в Википедии и показывает краткое описание.
- Интерфейс на русском и английском.

### Структура

```
back/
  space.py        API и расчёты
  unit_test.py    тесты
front/
  space_front.py  интерфейс
  vocab.py        переводы созвездий, планет и строк интерфейса
```

### Запуск

Установить зависимости:

```
pip install fastapi uvicorn ephem nicegui httpx pytest
```

Оба сервера работают по HTTPS и ищут `key.pem` и `cert.pem` в папке, из которой их запускают. Для локального запуска подойдёт самоподписанный сертификат:

```
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"
```

Положите оба файла в `back/` и `front/`, затем запустите в двух терминалах:

```
cd back
python space.py
```

```
cd front
python space_front.py
```

Бэкенд работает на `https://127.0.0.1:8000`, сайт открывается на `https://localhost:8080`.

### API

`GET /api/constellation/current` возвращает тело текущего часа и его созвездие.

`POST /api/calculation` возвращает созвездие в зените. Пример запроса:

```json
{"time_data": "2026/09/16 12:00:00", "lat": 55.75, "lon": 37.61}
```

Время указывается в UTC, широта и долгота в градусах (север и восток положительные).

### Тесты

```
cd back
pytest unit_test.py
```

## English

A web app that shows which constellation is at the zenith for a given date, time and location.

The backend is built with FastAPI, and the calculations use PyEphem. The frontend is built with NiceGUI.

### Features

- Finds the zenith constellation for a date, time (UTC), latitude and longitude.
- The home page shows one celestial body (Sun, Moon, Mars, Venus, Jupiter, Saturn, Uranus, Neptune; it changes every hour) and the constellation it is currently in.
- Searches Wikipedia and shows a short summary.
- English and Russian UI.

### Structure

```
back/
  space.py        API and calculations
  unit_test.py    tests
front/
  space_front.py  UI
  vocab.py        translations of constellations, planets and UI strings
```

### Running

Install dependencies:

```
pip install fastapi uvicorn ephem nicegui httpx pytest
```

Both servers run over HTTPS and look for `key.pem` and `cert.pem` in the directory they are started from. A self-signed certificate is fine for local use:

```
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"
```

Put both files in `back/` and `front/`, then start the servers in two terminals:

```
cd back
python space.py
```

```
cd front
python space_front.py
```

The backend runs at `https://127.0.0.1:8000` and the site at `https://localhost:8080`.

### API

`GET /api/constellation/current` returns the body of the current hour and its constellation.

`POST /api/calculation` returns the zenith constellation. Example request:

```json
{"time_data": "2026/09/16 12:00:00", "lat": 55.75, "lon": 37.61}
```

Time is in UTC. Latitude and longitude are in degrees, with north and east positive.

### Tests

```
cd back
pytest unit_test.py
```
