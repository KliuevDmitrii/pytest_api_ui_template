# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'git clone https://github.com/KliuevDmitrii/pytest_api_ui_template.git'
2. Установить зависимости 'pip3 install > -r requirements.txt'
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'

### Стек:
- pytest
- selenium
- webdriver manager 
- requests
- _sqlalchemy_
- allure
- configparser
- json

### Струткура:
- ./test - тесты
- ./page - описание страниц
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД
- ./configuration - провайдер настроек
    - test_config.ini - настройки для тестов
- ./testdata - провайдер тестовых данных
    - test_data.json

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)

---

### Пример `test_config.ini` , `test_data.json`

```ini
[ui]  
base_url=https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback...
timeout=4
boards_url=https://trello.com/u/ВАШ_АККАУНТ/boards

# chrome или ff (firefox)
browser_name=chrome

[api]  
base_url=https://api.trello.com/1
api_key=ВАШ_API_КЛЮЧ

---

```json
{
  "token": "ВАШ_ТОКЕН",
  "username": "ваш_логин",
  "email": "ваш_email@example.com",
  "pass": "ваш_пароль",
  "org_id": "ID_вашей_организации"
}

---
