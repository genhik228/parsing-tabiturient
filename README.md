# Парсинг данных абитуриентов с сайта "Табитуриент"

Проект предназначен для автоматизированного сбора и анализа данных о баллах абитуриентов из различных вузов страны. Собранная информация сохраняется в базу данных PostgreSQL для дальнейшего использования в аналитических целях.

## 📌 Основные функции
- Автоматизированный парсинг данных с сайта "Табитуриент" https://tabiturient.ru/.
- Сохранение структурированных данных (баллы, специальности, учебные заведения) в PostgreSQL.
- Поддержка динамических элементов сайта с использованием Selenium.
- Фильтрация и обработка данных перед сохранением.

## 🛠 Технологии
- **Python** (основной язык разработки).
- **Selenium** — для взаимодействия с динамическим контентом и автоматизации браузера.
- **BeautifulSoup4** — для парсинга HTML-страниц.
- **PostgreSQL** — хранение данных.
- **Psycopg2** — библиотека для работы с PostgreSQL из Python.

---

## 🚀 Установка и настройка

### Требования
- Python 3.9+
- Установленный PostgreSQL.
- Браузер Chrome и [ChromeDriver](https://chromedriver.chromium.org/) (для Selenium).

### Инструкция
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/genhik228/parsing-tabiturient
   cd parsing-tabiturient
   
2. **Cоздайте базу, используя файл table.sql:**
