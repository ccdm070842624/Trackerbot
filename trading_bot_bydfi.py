#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trackerbot - Automated Cryptocurrency Trading Bot for ByDFi Exchange

Provides technical analysis, trading signals, and Telegram bot integration
for cryptocurrency trading automation.

Author: Trackerbot Team
License: MIT
"""

import os
import time
import hmac
import hashlib
import logging
import requests
import pandas as pd
import talib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram.constants import ParseMode
import threading
import asyncio

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot_bydfi.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ByDFiExchange:
    """
    Адаптер для работы с API биржи ByDFi.

    Обеспечивает аутентификацию, получение рыночных данных,
    информации о балансе и других операций с биржей.
    """

    def __init__(self, api_key, api_secret, testnet=False):
        """
        Инициализация клиента ByDFi Exchange.

        Args:
            api_key (str): API ключ ByDFi
            api_secret (str): Секретный ключ для подписи запросов
            testnet (bool): Использовать testnet (True) или production (False)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        if testnet:
            self.base_url = 'https://api-cloud-testnet.bydfi.com'
        else:
            self.base_url = 'https://api-cloud.bydfi.com'

        logger.info(f"ByDFi Exchange инициализирован (testnet={testnet})")

    def _generate_signature(self, params_str):
        """
        Генерация HMAC SHA256 подписи для аутентификации.

        Args:
            params_str (str): Строка параметров для подписи

        Returns:
            str: Шестнадцатеричная подпись HMAC SHA256
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            params_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method, endpoint, params=None, signed=False):
        """
        Выполнение HTTP запроса к API ByDFi.

        Args:
            method (str): HTTP метод (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict): Параметры запроса
            signed (bool): Требуется ли подпись запроса

        Returns:
            dict or None: JSON ответ или None при ошибке
        """
        if params is None:
            params = {}

        url = f"{self.base_url}{endpoint}"
        headers = {'X-BX-APIKEY': self.api_key} if self.api_key else {}

        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['recvWindow'] = 5000

            # Сортировка параметров по алфавиту
            sorted_params = sorted(params.items())
            params_str = '&'.join([f"{k}={v}" for k, v in sorted_params])

            # Генерация подписи
            signature = self._generate_signature(params_str)
            params['signature'] = signature

        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, params=params, headers=headers, timeout=10)
            else:
                logger.error(f"Неподдерживаемый HTTP метод: {method}")
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к {endpoint}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return None

    def fetch_ticker(self, symbol):
        """
        Получение текущей цены и 24ч статистики для символа.

        Args:
            symbol (str): Торговая пара (например, 'BTC/USDT')

        Returns:
            dict or None: Данные тикера или None
        """
        symbol_formatted = symbol.replace('/', '')
        endpoint = '/spot/market/ticker'
        params = {'symbol': symbol_formatted}

        result = self._request('GET', endpoint, params, signed=False)

        if result and 'data' in result:
            return result['data']

        logger.error(f"Не удалось получить тикер для {symbol}")
        return None

    def fetch_ohlcv(self, symbol, timeframe='1h', limit=100):
        """
        Получение OHLCV (свечных) данных.

        Args:
            symbol (str): Торговая пара (например, 'BTC/USDT')
            timeframe (str): Таймфрейм ('1m', '5m', '1h', '1d', etc.)
            limit (int): Количество свечей

        Returns:
            pandas.DataFrame or None: DataFrame с OHLCV данными
        """
        symbol_formatted = symbol.replace('/', '')
        endpoint = '/spot/market/kline'
        params = {
            'symbol': symbol_formatted,
            'interval': timeframe,
            'limit': limit
        }

        result = self._request('GET', endpoint, params, signed=False)

        if result and 'data' in result:
            data = result['data']

            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume'
            ])

            # Конвертация типов
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)

            return df

        logger.error(f"Не удалось получить OHLCV для {symbol}")
        return None

    def fetch_balance(self):
        """
        Получение баланса аккаунта.

        Returns:
            dict or None: Данные баланса или None
        """
        endpoint = '/spot/accountList'
        result = self._request('GET', endpoint, signed=True)

        if result and 'data' in result:
            return result['data']

        logger.error("Не удалось получить баланс")
        return None

    def fetch_all_tickers(self):
        """
        Получение тикеров для всех торговых пар.

        Returns:
            list or None: Список всех тикеров
        """
        endpoint = '/spot/market/tickers'
        result = self._request('GET', endpoint, signed=False)

        if result and 'data' in result:
            return result['data']

        logger.error("Не удалось получить все тикеры")
        return None

    def get_new_listings(self, days=7):
        """
        Получение новых листингов (эвристика на основе доступных данных).

        Args:
            days (int): Количество дней для поиска новых монет

        Returns:
            list: Список новых листингов
        """
        all_tickers = self.fetch_all_tickers()

        if not all_tickers:
            return []

        # Примечание: это упрощенная эвристика
        # В реальности нужен доступ к данным о дате листинга
        new_listings = []

        for ticker in all_tickers[:10]:  # Берем топ-10 как пример
            if ticker.get('priceChangePercent'):
                new_listings.append(ticker)

        return new_listings


class TelegramBot:
    """
    Telegram бот для взаимодействия с пользователями.

    Предоставляет команды для проверки цен, анализа,
    баланса и других операций через Telegram интерфейс.
    """

    def __init__(self, token, chat_id, exchange):
        """
        Инициализация Telegram бота.

        Args:
            token (str): Токен Telegram бота
            chat_id (str): ID чата для уведомлений
            exchange (ByDFiExchange): Экземпляр биржи
        """
        self.token = token
        self.chat_id = chat_id
        self.exchange = exchange
        self.app = None

        logger.info("Telegram бот инициализирован")

    async def cmd_start(self, update: Update, context):
        """Команда /start - приветственное сообщение."""
        welcome_message = """
🤖 <b>Добро пожаловать в Trackerbot!</b>

Я помогу вам отслеживать криптовалютный рынок и получать торговые сигналы.

<b>Доступные команды:</b>
/help - Показать это сообщение
/menu - Интерактивное меню
/price SYMBOL - Цена криптовалюты (например: /price BTC)
/analyze SYMBOL - Технический анализ
/balance - Баланс аккаунта
/listings - Новые листинги
/top - Топ растущих монет

Просто напишите название монеты (например: BTC) для быстрой проверки цены!
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.HTML)

    async def cmd_help(self, update: Update, context):
        """Команда /help - справка по командам."""
        help_message = """
📚 <b>Справка по командам Trackerbot</b>

<b>Основные команды:</b>
/start - Начать работу с ботом
/menu - Интерактивное меню с кнопками
/price SYMBOL - Текущая цена и 24ч статистика
  Пример: /price BTCUSDT

/analyze SYMBOL - Полный технический анализ
  Включает: RSI, MACD, EMA, Bollinger Bands
  Пример: /analyze ETHUSDT

/balance - Показать баланс аккаунта
/listings - Новые листинги монет (за 7 дней)
/top - Топ-10 растущих криптовалют

<b>Быстрый доступ:</b>
Просто отправьте символ монеты без команды:
  BTC, ETH, SOL и т.д.

<b>Автоматические сигналы:</b>
Бот автоматически анализирует BTC/USDT каждый час
и отправляет уведомления при изменении сигнала.

Сигналы:
🟢 ПОКУПАТЬ - Индикаторы показывают восходящий тренд
🔴 ПРОДАВАТЬ - Индикаторы показывают нисходящий тренд
⚪ ДЕРЖАТЬ - Нейтральные показатели
        """
        await update.message.reply_text(help_message, parse_mode=ParseMode.HTML)

    async def cmd_menu(self, update: Update, context):
        """Команда /menu - интерактивное меню."""
        keyboard = [
            [
                InlineKeyboardButton("💰 Цена BTC", callback_data='price_BTC'),
                InlineKeyboardButton("📊 Анализ BTC", callback_data='analyze_BTC')
            ],
            [
                InlineKeyboardButton("💼 Баланс", callback_data='balance'),
                InlineKeyboardButton("🆕 Новые листинги", callback_data='listings')
            ],
            [
                InlineKeyboardButton("📈 Топ растущих", callback_data='top'),
                InlineKeyboardButton("❓ Помощь", callback_data='help')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '🎛️ <b>Главное меню</b>\n\nВыберите действие:',
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    async def cmd_price(self, update: Update, context):
        """Команда /price - получение цены."""
        if not context.args:
            await update.message.reply_text(
                "❌ Укажите символ монеты.\nПример: /price BTCUSDT"
            )
            return

        symbol = context.args[0].upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'

        ticker = self.exchange.fetch_ticker(symbol.replace('USDT', '/USDT'))

        if ticker:
            price = float(ticker.get('lastPrice', 0))
            change_24h = float(ticker.get('priceChangePercent', 0))
            high_24h = float(ticker.get('highPrice', 0))
            low_24h = float(ticker.get('lowPrice', 0))
            volume_24h = float(ticker.get('volume', 0))

            emoji = "🟢" if change_24h > 0 else "🔴" if change_24h < 0 else "⚪"

            message = f"""
{emoji} <b>{symbol}</b>

💵 Цена: ${price:,.2f}
📊 Изм. 24ч: {change_24h:+.2f}%
📈 Макс 24ч: ${high_24h:,.2f}
📉 Мин 24ч: ${low_24h:,.2f}
💹 Объем 24ч: {volume_24h:,.0f}

🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(f"❌ Не удалось получить данные для {symbol}")

    async def cmd_analyze(self, update: Update, context):
        """Команда /analyze - технический анализ."""
        if not context.args:
            await update.message.reply_text(
                "❌ Укажите символ монеты.\nПример: /analyze BTCUSDT"
            )
            return

        symbol = context.args[0].upper()
        if not symbol.endswith('USDT'):
            symbol += 'USDT'

        await update.message.reply_text(f"🔄 Анализирую {symbol}...")

        df = self.exchange.fetch_ohlcv(symbol.replace('USDT', '/USDT'), '1h', 100)

        if df is None or len(df) < 50:
            await update.message.reply_text(f"❌ Недостаточно данных для {symbol}")
            return

        # Расчет индикаторов
        df['rsi'] = talib.RSI(df['close'], timeperiod=14)
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(
            df['close'], fastperiod=12, slowperiod=26, signalperiod=9
        )
        df['ema_50'] = talib.EMA(df['close'], timeperiod=50)
        df['ema_200'] = talib.EMA(df['close'], timeperiod=200)
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(
            df['close'], timeperiod=20
        )

        last = df.iloc[-1]

        # Определение сигнала
        rsi = last['rsi']
        macd = last['macd']
        macd_signal = last['macdsignal']
        ema_50 = last['ema_50']
        ema_200 = last['ema_200']
        price = last['close']

        signal = "⚪ ДЕРЖАТЬ"
        if rsi < 30 and macd > macd_signal and ema_50 > ema_200:
            signal = "🟢 ПОКУПАТЬ (Сильный)"
        elif rsi < 40 and macd > macd_signal:
            signal = "🟢 ПОКУПАТЬ"
        elif rsi > 70 and macd < macd_signal and ema_50 < ema_200:
            signal = "🔴 ПРОДАВАТЬ (Сильный)"
        elif rsi > 60 and macd < macd_signal:
            signal = "🔴 ПРОДАВАТЬ"

        message = f"""
📊 <b>Технический анализ {symbol}</b>

💵 Цена: ${price:,.2f}

<b>Индикаторы:</b>
RSI (14): {rsi:.2f} {'(Перепродан)' if rsi < 30 else '(Перекуплен)' if rsi > 70 else ''}
MACD: {macd:.2f}
MACD Signal: {macd_signal:.2f}
EMA 50: ${ema_50:.2f}
EMA 200: ${ema_200:.2f}

<b>Тренд:</b> {'🟢 Бычий' if ema_50 > ema_200 else '🔴 Медвежий'}

<b>Сигнал:</b> {signal}

🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    async def cmd_balance(self, update: Update, context):
        """Команда /balance - баланс аккаунта."""
        balance = self.exchange.fetch_balance()

        if balance:
            message = "💼 <b>Баланс аккаунта:</b>\n\n"

            for asset in balance:
                free = float(asset.get('free', 0))
                locked = float(asset.get('locked', 0))
                coin = asset.get('coin', 'Unknown')

                if free > 0 or locked > 0:
                    message += f"<b>{coin}:</b>\n"
                    message += f"  Доступно: {free:.8f}\n"
                    message += f"  Заблокировано: {locked:.8f}\n\n"

            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("❌ Не удалось получить баланс")

    async def cmd_new_listings(self, update: Update, context):
        """Команда /listings - новые листинги."""
        await update.message.reply_text("🔄 Получаю новые листинги...")

        listings = self.exchange.get_new_listings(7)

        if listings:
            message = "🆕 <b>Новые листинги (7 дней):</b>\n\n"

            for listing in listings[:10]:
                symbol = listing.get('symbol', 'Unknown')
                price = float(listing.get('lastPrice', 0))
                change = float(listing.get('priceChangePercent', 0))
                emoji = "🟢" if change > 0 else "🔴"

                message += f"{emoji} <b>{symbol}</b>\n"
                message += f"  Цена: ${price:.8f}\n"
                message += f"  Изм. 24ч: {change:+.2f}%\n\n"

            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("❌ Не удалось получить новые листинги")

    async def cmd_top_gainers(self, update: Update, context):
        """Команда /top - топ растущих монет."""
        await update.message.reply_text("🔄 Получаю топ растущих монет...")

        all_tickers = self.exchange.fetch_all_tickers()

        if all_tickers:
            # Сортировка по изменению цены
            sorted_tickers = sorted(
                all_tickers,
                key=lambda x: float(x.get('priceChangePercent', 0)),
                reverse=True
            )

            message = "📈 <b>Топ-10 растущих монет (24ч):</b>\n\n"

            for i, ticker in enumerate(sorted_tickers[:10], 1):
                symbol = ticker.get('symbol', 'Unknown')
                price = float(ticker.get('lastPrice', 0))
                change = float(ticker.get('priceChangePercent', 0))

                message += f"{i}. <b>{symbol}</b>\n"
                message += f"   Цена: ${price:.8f}\n"
                message += f"   🟢 +{change:.2f}%\n\n"

            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("❌ Не удалось получить данные")

    async def handle_text(self, update: Update, context):
        """Обработка текстовых сообщений (быстрая проверка цены)."""
        text = update.message.text.upper().strip()

        # Проверка, является ли текст символом монеты
        if len(text) <= 10 and text.isalpha():
            symbol = text
            if not symbol.endswith('USDT'):
                symbol += 'USDT'

            ticker = self.exchange.fetch_ticker(symbol.replace('USDT', '/USDT'))

            if ticker:
                price = float(ticker.get('lastPrice', 0))
                change_24h = float(ticker.get('priceChangePercent', 0))
                emoji = "🟢" if change_24h > 0 else "🔴"

                message = f"{emoji} <b>{symbol}</b>: ${price:,.2f} ({change_24h:+.2f}%)"
                await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(
                    f"❌ Монета {text} не найдена.\n"
                    "Используйте /help для списка команд."
                )

    async def button_callback(self, update: Update, context):
        """Обработка нажатий на кнопки."""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data.startswith('price_'):
            symbol = data.split('_')[1] + 'USDT'
            ticker = self.exchange.fetch_ticker(symbol.replace('USDT', '/USDT'))

            if ticker:
                price = float(ticker.get('lastPrice', 0))
                change_24h = float(ticker.get('priceChangePercent', 0))
                emoji = "🟢" if change_24h > 0 else "🔴"

                message = f"{emoji} <b>{symbol}</b>: ${price:,.2f} ({change_24h:+.2f}%)"
                await query.message.reply_text(message, parse_mode=ParseMode.HTML)

        elif data == 'balance':
            balance = self.exchange.fetch_balance()
            if balance:
                message = "💼 <b>Баланс:</b>\n\n"
                for asset in balance[:5]:
                    coin = asset.get('coin', 'Unknown')
                    free = float(asset.get('free', 0))
                    message += f"{coin}: {free:.8f}\n"
                await query.message.reply_text(message, parse_mode=ParseMode.HTML)

        elif data == 'help':
            await self.cmd_help(query, context)

    async def send_notification(self, message):
        """
        Отправка уведомления в Telegram.

        Args:
            message (str): Текст сообщения
        """
        try:
            await self.app.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")

    def run(self):
        """Запуск Telegram бота."""
        self.app = Application.builder().token(self.token).build()

        # Регистрация обработчиков команд
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("menu", self.cmd_menu))
        self.app.add_handler(CommandHandler("price", self.cmd_price))
        self.app.add_handler(CommandHandler("analyze", self.cmd_analyze))
        self.app.add_handler(CommandHandler("balance", self.cmd_balance))
        self.app.add_handler(CommandHandler("listings", self.cmd_new_listings))
        self.app.add_handler(CommandHandler("top", self.cmd_top_gainers))

        # Обработчики кнопок и текста
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

        logger.info("Telegram бот запущен")
        self.app.run_polling()


class TradingBot:
    """
    Главный класс торгового бота.

    Координирует анализ рынка, генерацию сигналов и уведомления.
    """

    def __init__(self, exchange, telegram_bot, symbol='BTC/USDT', timeframe='1h'):
        """
        Инициализация торгового бота.

        Args:
            exchange (ByDFiExchange): Экземпляр биржи
            telegram_bot (TelegramBot): Экземпляр Telegram бота
            symbol (str): Торговая пара для анализа
            timeframe (str): Таймфрейм для анализа
        """
        self.exchange = exchange
        self.telegram_bot = telegram_bot
        self.symbol = symbol
        self.timeframe = timeframe
        self.last_signal = None
        self.signals_history = []

        logger.info(f"TradingBot инициализирован для {symbol} ({timeframe})")

    def get_data(self):
        """
        Получение рыночных данных.

        Returns:
            pandas.DataFrame or None: OHLCV данные
        """
        logger.info(f"Получение данных для {self.symbol}")
        return self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=100)

    def calculate_indicators(self, df):
        """
        Расчет технических индикаторов.

        Args:
            df (pandas.DataFrame): DataFrame с OHLCV данными

        Returns:
            pandas.DataFrame: DataFrame с добавленными индикаторами
        """
        logger.info("Расчет технических индикаторов")

        # RSI
        df['rsi'] = talib.RSI(df['close'], timeperiod=14)

        # MACD
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(
            df['close'],
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )

        # EMA
        df['ema_50'] = talib.EMA(df['close'], timeperiod=50)
        df['ema_200'] = talib.EMA(df['close'], timeperiod=200)

        # Bollinger Bands
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(
            df['close'],
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2
        )

        return df

    def analyze(self, df):
        """
        Анализ данных и генерация торгового сигнала.

        Args:
            df (pandas.DataFrame): DataFrame с индикаторами

        Returns:
            tuple: (сигнал, метрики)
        """
        last = df.iloc[-1]
        prev = df.iloc[-2]

        rsi = last['rsi']
        macd = last['macd']
        macd_signal = last['macdsignal']
        macd_prev = prev['macd']
        macd_signal_prev = prev['macdsignal']
        ema_50 = last['ema_50']
        ema_200 = last['ema_200']
        price = last['close']

        # MACD пересечение
        macd_crossover_up = macd > macd_signal and macd_prev <= macd_signal_prev
        macd_crossover_down = macd < macd_signal and macd_prev >= macd_signal_prev

        # Определение тренда
        trend_bullish = ema_50 > ema_200
        trend_bearish = ema_50 < ema_200

        # Генерация сигнала
        signal = "ДЕРЖАТЬ"

        # Сильный сигнал ПОКУПАТЬ
        if rsi < 30 and macd_crossover_up and trend_bullish:
            signal = "ПОКУПАТЬ (Сильный)"
        # Обычный сигнал ПОКУПАТЬ
        elif (rsi < 40 and macd_crossover_up) or (rsi < 30 and trend_bullish):
            signal = "ПОКУПАТЬ"
        # Сильный сигнал ПРОДАВАТЬ
        elif rsi > 70 and macd_crossover_down and trend_bearish:
            signal = "ПРОДАВАТЬ (Сильный)"
        # Обычный сигнал ПРОДАВАТЬ
        elif (rsi > 60 and macd_crossover_down) or (rsi > 70 and trend_bearish):
            signal = "ПРОДАВАТЬ"

        metrics = {
            'price': price,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': macd_signal,
            'ema_50': ema_50,
            'ema_200': ema_200,
            'trend': 'Бычий' if trend_bullish else 'Медвежий' if trend_bearish else 'Нейтральный'
        }

        logger.info(f"Сигнал: {signal}, Цена: {price:.2f}, RSI: {rsi:.2f}")

        return signal, metrics

    async def send_signal_notification(self, signal, metrics):
        """
        Отправка уведомления о сигнале.

        Args:
            signal (str): Торговый сигнал
            metrics (dict): Метрики анализа
        """
        emoji_map = {
            'ПОКУПАТЬ (Сильный)': '🟢🟢',
            'ПОКУПАТЬ': '🟢',
            'ПРОДАВАТЬ (Сильный)': '🔴🔴',
            'ПРОДАВАТЬ': '🔴',
            'ДЕРЖАТЬ': '⚪'
        }

        emoji = emoji_map.get(signal, '⚪')

        message = f"""
{emoji} <b>ТОРГОВЫЙ СИГНАЛ</b> {emoji}

<b>Символ:</b> {self.symbol}
<b>Сигнал:</b> {signal}

<b>Цена:</b> ${metrics['price']:,.2f}
<b>RSI:</b> {metrics['rsi']:.2f}
<b>MACD:</b> {metrics['macd']:.2f}
<b>Тренд:</b> {metrics['trend']}

🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        await self.telegram_bot.send_notification(message)

    async def run_analysis_loop(self, check_interval=3600):
        """
        Запуск цикла анализа.

        Args:
            check_interval (int): Интервал проверки в секундах (по умолчанию 1 час)
        """
        logger.info(f"Запуск цикла анализа (интервал: {check_interval}с)")

        while True:
            try:
                df = self.get_data()

                if df is not None and len(df) >= 50:
                    df = self.calculate_indicators(df)
                    signal, metrics = self.analyze(df)

                    # Отправка уведомления только при изменении сигнала
                    if signal != self.last_signal:
                        logger.info(f"Сигнал изменился: {self.last_signal} → {signal}")
                        await self.send_signal_notification(signal, metrics)
                        self.last_signal = signal

                        # Сохранение в историю
                        self.signals_history.append({
                            'timestamp': datetime.now(),
                            'signal': signal,
                            'price': metrics['price']
                        })
                else:
                    logger.warning(f"Недостаточно данных для {self.symbol}")

            except Exception as e:
                logger.error(f"Ошибка в цикле анализа: {e}")

            await asyncio.sleep(check_interval)

    def run(self):
        """Запуск бота (Telegram бот в отдельном потоке + цикл анализа)."""
        # Запуск Telegram бота в отдельном потоке
        telegram_thread = threading.Thread(target=self.telegram_bot.run, daemon=True)
        telegram_thread.start()

        logger.info("Telegram бот запущен в отдельном потоке")

        # Даем время на инициализацию Telegram бота
        time.sleep(5)

        # Запуск цикла анализа в основном потоке
        try:
            asyncio.run(self.run_analysis_loop(check_interval=3600))
        except KeyboardInterrupt:
            logger.info("Остановка бота по Ctrl+C")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")


def main():
    """Главная функция запуска бота."""
    logger.info("=" * 50)
    logger.info("Запуск Trackerbot")
    logger.info("=" * 50)

    # Загрузка конфигурации из переменных окружения
    BYDFI_API_KEY = os.getenv('BYDFI_API_KEY')
    BYDFI_API_SECRET = os.getenv('BYDFI_API_SECRET')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    # Проверка наличия обязательных переменных
    if not all([BYDFI_API_KEY, BYDFI_API_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        logger.error("❌ Не все обязательные переменные окружения установлены!")
        logger.error("Требуются: BYDFI_API_KEY, BYDFI_API_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return

    # Инициализация компонентов
    exchange = ByDFiExchange(
        api_key=BYDFI_API_KEY,
        api_secret=BYDFI_API_SECRET,
        testnet=True  # Измените на False для production
    )

    telegram_bot = TelegramBot(
        token=TELEGRAM_BOT_TOKEN,
        chat_id=TELEGRAM_CHAT_ID,
        exchange=exchange
    )

    trading_bot = TradingBot(
        exchange=exchange,
        telegram_bot=telegram_bot,
        symbol='BTC/USDT',
        timeframe='1h'
    )

    # Запуск бота
    logger.info("Все компоненты инициализированы, запуск...")
    trading_bot.run()


if __name__ == '__main__':
    main()
