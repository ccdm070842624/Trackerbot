# 🤖 Trackerbot

> Автоматизированный торговый бот для криптовалют с интеграцией ByDFi биржи и Telegram

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Описание

Trackerbot - это автоматизированный торговый бот, который подключается к бирже ByDFi и предоставляет:

- 📊 **Технический анализ** - RSI, MACD, EMA, Bollinger Bands
- 🎯 **Торговые сигналы** - Автоматическая генерация сигналов на покупку/продажу
- 💬 **Telegram бот** - Интерактивный интерфейс для управления и мониторинга
- 🆕 **Отслеживание новых листингов** - Мониторинг новых монет на бирже
- 📈 **Топ растущих монет** - Анализ лучших исполнителей рынка

## ✨ Возможности

### Технический анализ
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- EMA (Exponential Moving Average) - 50 и 200 периодов
- Bollinger Bands
- Определение трендов

### Торговые сигналы
- 🟢 **ПОКУПАТЬ** - Индикаторы перепроданы, восходящий тренд
- 🔴 **ПРОДАВАТЬ** - Индикаторы перекуплены, нисходящий тренд
- ⚪ **ДЕРЖАТЬ** - Нейтральные условия

### Telegram команды
- `/start` - Приветственное сообщение
- `/help` - Справка по командам
- `/menu` - Интерактивное меню
- `/price SYMBOL` - Текущая цена монеты
- `/analyze SYMBOL` - Полный технический анализ
- `/balance` - Баланс аккаунта
- `/listings` - Новые листинги
- `/top` - Топ растущих монет

## 🚀 Быстрый старт

### Требования

- Python 3.8 или выше
- ByDFi API ключи ([получить здесь](https://www.bydfi.com/))
- Telegram бот токен (получить у [@BotFather](https://t.me/BotFather))
- TA-Lib системная библиотека

### Установка

#### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/Trackerbot.git
cd Trackerbot
```

#### 2. Установка системных зависимостей

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ta-lib python3-dev build-essential
```

**macOS:**
```bash
brew install ta-lib
```

**Windows:**
Скачайте предкомпилированные бинарники TA-Lib с [неофициального сайта](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)

#### 3. Установка Python зависимостей

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Настройка переменных окружения

```bash
# Создание .env файла из шаблона
cp .env.example .env

# Редактирование .env файла
nano .env  # или любой другой редактор
```

Заполните следующие переменные:

```env
BYDFI_API_KEY=ваш_api_ключ
BYDFI_API_SECRET=ваш_api_секрет
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
```

**Как получить учетные данные:**

1. **ByDFi API:**
   - Зарегистрируйтесь на [ByDFi](https://www.bydfi.com/)
   - Перейдите в API Management
   - Создайте новый API ключ (для тестирования выбирайте read-only)

2. **Telegram Bot Token:**
   - Напишите [@BotFather](https://t.me/BotFather)
   - Отправьте `/newbot` и следуйте инструкциям
   - Скопируйте полученный токен

3. **Telegram Chat ID:**
   - Напишите [@userinfobot](https://t.me/userinfobot)
   - Скопируйте ваш ID

#### 5. Запуск бота

```bash
# Запуск в режиме testnet (рекомендуется для начала)
python trading_bot_bydfi.py
```

**Важно:** По умолчанию бот работает в режиме testnet. Для работы с production измените `testnet=True` на `testnet=False` в файле `trading_bot_bydfi.py` (строка 788).

## 📖 Использование

### Telegram команды

После запуска бота откройте Telegram и найдите вашего бота:

1. **Начало работы:**
   ```
   /start
   ```

2. **Проверка цены:**
   ```
   /price BTC
   /price ETHUSDT
   ```
   Или просто напишите название монеты:
   ```
   BTC
   ETH
   ```

3. **Технический анализ:**
   ```
   /analyze BTC
   /analyze ETHUSDT
   ```

4. **Интерактивное меню:**
   ```
   /menu
   ```

5. **Баланс аккаунта:**
   ```
   /balance
   ```

6. **Новые листинги:**
   ```
   /listings
   ```

7. **Топ растущих монет:**
   ```
   /top
   ```

### Автоматические уведомления

Бот автоматически анализирует BTC/USDT каждый час и отправляет уведомления при изменении торгового сигнала:

- 🟢🟢 **ПОКУПАТЬ (Сильный)** - Все 3 условия выполнены (RSI < 30, MACD пересечение вверх, бычий тренд)
- 🟢 **ПОКУПАТЬ** - 2 из 3 условий выполнены
- 🔴🔴 **ПРОДАВАТЬ (Сильный)** - Все 3 условия выполнены (RSI > 70, MACD пересечение вниз, медвежий тренд)
- 🔴 **ПРОДАВАТЬ** - 2 из 3 условий выполнены
- ⚪ **ДЕРЖАТЬ** - Нейтральные условия

## ⚙️ Конфигурация

### Изменение торговой пары

По умолчанию бот анализирует BTC/USDT. Для изменения отредактируйте `trading_bot_bydfi.py`:

```python
trading_bot = TradingBot(
    exchange=exchange,
    telegram_bot=telegram_bot,
    symbol='ETH/USDT',  # Измените здесь
    timeframe='1h'
)
```

### Изменение интервала проверки

По умолчанию анализ проводится каждый час (3600 секунд). Для изменения:

```python
await self.run_analysis_loop(check_interval=1800)  # 30 минут
```

### Переключение на production

1. Получите production API ключи от ByDFi
2. Обновите `.env` файл с production ключами
3. В `trading_bot_bydfi.py` измените:

```python
exchange = ByDFiExchange(
    api_key=BYDFI_API_KEY,
    api_secret=BYDFI_API_SECRET,
    testnet=False  # Изменить на False
)
```

## 🔒 Безопасность

- ⚠️ **НИКОГДА** не коммитьте `.env` файл в git
- 🔐 Используйте read-only API ключи для тестирования
- 🔄 Регулярно меняйте API ключи
- 🧪 Всегда тестируйте на testnet перед production
- 📝 Ограничьте права доступа API ключей (только чтение для анализа)

## 📊 Логирование

Все события логируются в файл `trading_bot_bydfi.log` и консоль:

```bash
# Просмотр логов в реальном времени
tail -f trading_bot_bydfi.log

# Поиск ошибок
grep "ERROR" trading_bot_bydfi.log

# Поиск сигналов
grep "Сигнал" trading_bot_bydfi.log
```

## 🐛 Решение проблем

### TA-Lib не устанавливается

```bash
# Ubuntu/Debian - установка из исходников
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

### Telegram бот не отвечает

1. Проверьте токен бота: `curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"`
2. Убедитесь, что не запущен другой экземпляр: `ps aux | grep trading_bot_bydfi.py`
3. Проверьте права доступа бота в Telegram

### API ошибки

1. Проверьте время на сервере: `date`
2. Синхронизируйте время: `sudo ntpdate -s time.nist.gov`
3. Проверьте правильность API ключей
4. Убедитесь, что используете правильный endpoint (testnet/production)

## 📚 Документация

- [CLAUDE.md](CLAUDE.md) - Документация для AI ассистентов
- [ByDFi API Docs](https://bydfi-api-docs.com/) - Документация API биржи
- [python-telegram-bot](https://docs.python-telegram-bot.org/) - Документация Telegram бота
- [TA-Lib](https://mrjbq7.github.io/ta-lib/) - Документация технического анализа

## 🚧 Roadmap

- [ ] Добавить unit тесты
- [ ] Реализовать базу данных для хранения истории сигналов
- [ ] Добавить поддержку нескольких торговых пар
- [ ] Реализовать веб-интерфейс для мониторинга
- [ ] Добавить backtesting функциональность
- [ ] Интеграция с другими биржами
- [ ] Реализация автоматического исполнения сделок (с подтверждением)

## 🤝 Вклад в проект

Приветствуются pull requests! Для значительных изменений:

1. Откройте issue для обсуждения изменений
2. Создайте форк репозитория
3. Создайте feature ветку (`git checkout -b feature/AmazingFeature`)
4. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
5. Отправьте в ветку (`git push origin feature/AmazingFeature`)
6. Откройте Pull Request

## ⚠️ Отказ от ответственности

Этот бот предназначен только для образовательных целей и анализа рынка. Не является финансовым советом. Автоматическая торговля криптовалютами связана с высоким риском. Используйте на свой страх и риск.

**НИКОГДА** не торгуйте средствами, которые вы не можете позволить себе потерять.

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 👥 Авторы

- Trackerbot Team

## 🙏 Благодарности

- [ByDFi](https://www.bydfi.com/) - За предоставление API
- [TA-Lib](https://ta-lib.org/) - За библиотеку технического анализа
- [python-telegram-bot](https://python-telegram-bot.org/) - За отличный Telegram фреймворк

---

**⭐ Если этот проект вам помог, поставьте звезду на GitHub!**
