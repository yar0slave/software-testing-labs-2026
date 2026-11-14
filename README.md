# Лабораторные работы по тестированию ПО

Учебные приложения и тесты для ЛР 1–9. Python 3.12.

## Быстрый запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Во втором терминале: `python -m pytest --junitxml=evidence/results.xml`.
Стенды: http://127.0.0.1:8765/calculator.html, /todo.html, /login.html, /contact.html.
Демонстрационный вход: student / Test123! (не реальные учётные данные).
Todo содержит намеренные дефекты; `todo.html?fixed=1` включает исправления.
Тесты исходной версии подтверждают наличие учебных дефектов, а не её корректность.

## Selenium в Docker

```bash
docker run -d --name lab-selenium --shm-size=2g -p 127.0.0.1:4444:4444 -v "$PWD:/opt/labs:ro" selenium/standalone-chromium:latest
docker exec -d lab-selenium python3 /opt/labs/server.py
SELENIUM_URL=http://127.0.0.1:4444 python -m pytest
```

Обычный запуск использует локальный Chrome и Selenium Manager.
В Docker тестируемые страницы открываются внутри контейнера на порту 8765.

## Postman и API

Импортировать `postman/users.postman_collection.json` в Postman и выполнить Run collection.
CLI-эквивалент: `npx newman run postman/users.postman_collection.json`.
Python: `python -m pytest tests/test_api.py`.
JSONPlaceholder имитирует запись: POST и PUT не сохраняют изменения в базе.

## Нагрузка

```bash
k6 run --vus 10 --duration 30s --summary-export evidence/k6-10.json load/health.js
k6 run --vus 50 --duration 10s --summary-export evidence/k6-50.json load/health.js
```

Нагрузка направляется только на локальный учебный API. Перед запуском включить `server.py`.

## Android и Appium

Собственное приложение находится в `mobile/`, установочный файл — `lab-notes.apk`.
Сборка: JDK 17, Android SDK platform 35 и build-tools 35.0.0; задать JAVA_HOME и ANDROID_HOME, выполнить `bash mobile/build.sh`.
Запустить Android-эмулятор, затем `appium driver install uiautomator2` и `appium`.
Тест: `python -m pytest mobile/test_appium.py`.
Для драйвера использована совместимая с Appium 3 версия UiAutomator2 8.7.3.

## CI

`.github/workflows/run-tests.yml` запускает модульные и UI-тесты на push, pull_request и вручную.
API-тесты внешнего сервиса выполняются отдельно, чтобы доступность чужого API не влияла на результат проверки собственного приложения.
Логи и скриншоты загружаются как artifact `test-evidence`.
