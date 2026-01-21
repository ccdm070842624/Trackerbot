# CLAUDE.md - AI Assistant Documentation for Trackerbot

> **Last Updated:** 2026-01-21
> **Repository:** Trackerbot
> **Purpose:** Comprehensive guide for AI assistants working on this codebase

---

## Table of Contents

1. [About This Document](#about-this-document)
2. [Project Overview](#project-overview)
3. [Repository Structure](#repository-structure)
4. [Technology Stack](#technology-stack)
5. [Development Workflow](#development-workflow)
6. [Code Conventions & Standards](#code-conventions--standards)
7. [Architecture & Design Patterns](#architecture--design-patterns)
8. [Key Components](#key-components)
9. [Testing Strategy](#testing-strategy)
10. [Deployment & CI/CD](#deployment--cicd)
11. [Common Tasks](#common-tasks)
12. [Troubleshooting](#troubleshooting)
13. [Important Notes for AI Assistants](#important-notes-for-ai-assistants)

---

## About This Document

This document is specifically designed for AI assistants (like Claude) to understand the Trackerbot codebase, development practices, and project conventions. It should be **kept up-to-date** as the project evolves.

### When to Update This Document

- After significant architectural changes
- When adding new major features or components
- When changing development workflows or conventions
- When updating dependencies or technology stack
- At least once per major version release

---

## Project Overview

### What is Trackerbot?

**Status:** 🚀 Active Development

Trackerbot is an automated cryptocurrency trading bot that connects to the ByDFi exchange and provides technical analysis, trading signals, and interactive Telegram bot integration for cryptocurrency trading automation.

### Project Goals

- Provide automated technical analysis for cryptocurrency pairs on ByDFi exchange
- Generate real-time trading signals based on RSI, MACD, and EMA indicators
- Offer interactive Telegram bot interface for manual queries and market monitoring
- Track new listings and top-performing cryptocurrencies
- Enable automated monitoring with customizable alert thresholds

### Key Features

- **ByDFi Exchange Integration**: Full API integration with ByDFi (supports testnet and production)
- **Technical Analysis Engine**: RSI, MACD, EMA, Bollinger Bands calculations using TA-Lib
- **Telegram Bot Interface**: Interactive commands and inline buttons for user queries
- **Automated Signal Generation**: Hourly analysis with push notifications for signal changes
- **Market Monitoring**: New listings tracking and top gainers identification
- **Real-time Price Tracking**: Live price feeds and 24h statistics

---

## Repository Structure

**Current Status:** Monolithic Python application

### Current Directory Structure

```
Trackerbot/
├── .env                      # Environment variables (not committed)
├── .gitignore               # Git ignore patterns
├── trading_bot_bydfi.py     # Main application (all-in-one)
├── trading_bot_bydfi.log    # Application logs
├── requirements.txt         # Python dependencies
├── README.md                # User-facing documentation
└── CLAUDE.md                # This file - AI assistant documentation
```

### Future Recommended Structure

For better maintainability, consider refactoring to:

```
Trackerbot/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── exchange/
│   │   ├── __init__.py
│   │   └── bydfi.py         # ByDFiExchange class
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── telegram_bot.py  # TelegramBot class
│   │   └── trading_bot.py   # TradingBot class
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── indicators.py    # Technical analysis functions
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logging configuration
├── tests/                   # Unit and integration tests
├── .env.example            # Example environment variables
├── .gitignore
├── requirements.txt
├── README.md
└── CLAUDE.md
```

### Important Files & Directories

| Path | Purpose | Notes |
|------|---------|-------|
| `trading_bot_bydfi.py` | Main application with all classes | Monolithic design - consider refactoring |
| `.env` | Environment variables | **NEVER COMMIT** - contains API keys |
| `trading_bot_bydfi.log` | Application logs | Rotated, not committed |
| `CLAUDE.md` | AI assistant documentation | Keep updated with changes |
| `requirements.txt` | Python dependencies | Pin versions for stability |

---

## Technology Stack

### Core Technologies

- **Language:** Python 3.8+ (asyncio support required)
- **Exchange API:** ByDFi REST API (testnet and production)
- **Bot Framework:** python-telegram-bot (v20+)
- **Technical Analysis:** TA-Lib (Technical Analysis Library)
- **Data Processing:** pandas, numpy

### Development Tools

- **Version Control:** Git
- **Repository Host:** GitHub
- **Package Manager:** pip
- **Environment Management:** python-dotenv
- **Testing Framework:** TBD (pytest recommended)
- **Linting/Formatting:** TBD (black, flake8, pylint recommended)

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | Latest | Data manipulation and OHLCV handling |
| `TA-Lib` | Latest | Technical indicators (RSI, MACD, EMA, BB) |
| `requests` | Latest | HTTP requests to ByDFi API |
| `python-telegram-bot` | 20+ | Telegram bot interface |
| `python-dotenv` | Latest | Environment variable management |

### System Dependencies

- **TA-Lib C Library**: Must be installed at system level before pip install
  ```bash
  # Ubuntu/Debian
  sudo apt-get install ta-lib

  # macOS
  brew install ta-lib
  ```

---

## Development Workflow

### Branch Strategy

**Branch Naming Convention:**
- Feature branches: `claude/[feature-description]-[session-id]`
- Bug fixes: `claude/fix-[issue-description]-[session-id]`
- Documentation: `claude/docs-[description]-[session-id]`

**Example:** `claude/add-user-authentication-ABC123`

### Git Workflow

1. **Create/Switch to Branch**
   ```bash
   git checkout -b claude/[feature-name]-[session-id]
   ```

2. **Make Changes**
   - Follow code conventions
   - Write tests for new functionality
   - Update documentation

3. **Commit Changes**
   ```bash
   git add [files]
   git commit -m "Clear, descriptive commit message"
   ```

4. **Push to Remote**
   ```bash
   git push -u origin claude/[branch-name]
   ```
   - ⚠️ **Critical:** Branch must start with `claude/` and match session ID
   - Retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s) if network fails

5. **Create Pull Request**
   - Use `gh pr create` for GitHub CLI
   - Include clear title and description
   - Reference any related issues

### Commit Message Guidelines

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Example:**
```
feat(auth): add JWT token validation

Implement middleware to validate JWT tokens for protected routes.
Includes token expiry checking and refresh token support.

Closes #123
```

---

## Code Conventions & Standards

### General Principles

1. **Clarity over Cleverness:** Write clear, readable code
2. **YAGNI:** You Aren't Gonna Need It - don't over-engineer
3. **DRY:** Don't Repeat Yourself (but avoid premature abstraction)
4. **Single Responsibility:** Each module/function should do one thing well
5. **Fail Fast:** Validate inputs early and fail with clear error messages

### Naming Conventions

**Python PEP 8 Style:**

- **Variables:** snake_case - `last_rsi`, `check_interval`
- **Functions:** snake_case with verbs - `get_data()`, `calculate_indicators()`
- **Classes:** PascalCase - `ByDFiExchange`, `TelegramBot`, `TradingBot`
- **Constants:** UPPER_SNAKE_CASE - `BYDFI_API_KEY`, `RSI_OVERSOLD`
- **Private methods:** Leading underscore - `_request()`, `_generate_signature()`
- **Async functions:** Use `async def` prefix clearly

### Code Style

**Current (should be formalized):**

- Indentation: 4 spaces (Python standard)
- Line length: ~80-120 characters (inconsistent)
- String quotes: Single quotes preferred, but inconsistent
- Docstrings: Triple double-quotes, but sparse
- Type hints: Not used (should add)

**Recommended:**

- Use `black` formatter (88 char line length)
- Use `flake8` linter
- Use `mypy` for type checking
- Add type hints to all function signatures
- Add docstrings to all public methods

### Comments & Documentation

- **Code Comments:** Use sparingly - code should be self-documenting
- **Docstrings:** Required for all public functions, classes, and modules
- **TODOs:** Use `TODO:` comments with issue references
- **Complex Logic:** Explain the "why", not the "what"

### Error Handling

- Always validate external inputs
- Use specific error types
- Include context in error messages
- Log errors appropriately
- Don't catch errors you can't handle

### Security Guidelines

**Always check for:**
- Command injection vulnerabilities
- SQL injection (use parameterized queries)
- XSS vulnerabilities (sanitize user input)
- CSRF protection
- Authentication & authorization
- Secure credential storage
- Input validation at system boundaries

---

## Architecture & Design Patterns

### Architectural Approach

**Current:** Monolithic single-file application with three main classes
- Simple, straightforward design for rapid development
- All components in one file: `trading_bot_bydfi.py`
- Suitable for small-scale deployment

**Recommended Future:** Modular architecture with separation of concerns
- Exchange adapter pattern for ByDFi API
- Bot services layer (Telegram, Trading Analysis)
- Separate technical analysis module

### Design Patterns Used

- **Adapter Pattern**: `ByDFiExchange` class abstracts exchange-specific API details
- **Command Pattern**: Telegram bot command handlers (`CommandHandler`, `CallbackQueryHandler`)
- **Observer Pattern**: Implicit - bot observes market changes and notifies users
- **Strategy Pattern**: Analysis logic is encapsulated and can be swapped
- **Singleton-like**: Single bot instance manages all operations

### Data Flow

```
1. Market Data Acquisition:
   ByDFi API → ByDFiExchange.fetch_ohlcv() → pandas DataFrame

2. Technical Analysis:
   DataFrame → TA-Lib indicators → Analysis metrics → Trading signal

3. Signal Generation:
   TradingBot.analyze() → Signal (BUY/SELL/HOLD) → Metrics dict

4. User Notification:
   Signal change detected → TradingBot.send_signal_notification()
   → TelegramBot.send_notification() → User

5. Interactive Queries:
   User → Telegram command → TelegramBot handler
   → ByDFiExchange API call → Formatted response → User
```

### API Design

**ByDFi API Authentication:**
- HMAC SHA256 signature-based authentication
- Timestamp and recvWindow parameters for replay protection
- API key in `X-BX-APIKEY` header
- Signature in request parameters

**Telegram Bot API:**
- Webhook mode: Not currently implemented
- Polling mode: Active (long-polling for updates)
- Async/await pattern for handlers

---

## Key Components

### Component Overview

| Component | Purpose | Location | Dependencies |
|-----------|---------|----------|--------------|
| `ByDFiExchange` | Exchange API adapter | trading_bot_bydfi.py:31-226 | requests, hmac, hashlib |
| `TelegramBot` | User interface bot | trading_bot_bydfi.py:229-621 | python-telegram-bot |
| `TradingBot` | Main orchestrator | trading_bot_bydfi.py:624-789 | ByDFiExchange, TelegramBot |

### Component Details

#### ByDFiExchange

- **Purpose:** Encapsulates all ByDFi API interactions
- **Location:** `trading_bot_bydfi.py` lines 31-226
- **Key Methods:**
  - `fetch_ohlcv(symbol, timeframe, limit)` - Get candlestick data
  - `fetch_balance()` - Get account balances
  - `fetch_ticker(symbol)` - Get current price and 24h stats
  - `fetch_all_tickers()` - Get all market tickers
  - `get_new_listings(days)` - Get new coin listings (heuristic)
  - `_request(method, endpoint, params, signed)` - Internal HTTP request handler
  - `_generate_signature(params_str)` - HMAC-SHA256 signature generation
- **Authentication:**
  - API key: From `BYDFI_API_KEY` environment variable
  - API secret: From `BYDFI_API_SECRET` environment variable
  - Testnet support via constructor parameter
- **Error Handling:**
  - Returns `None` on API errors
  - Logs errors but doesn't raise exceptions
  - Request timeout: 10 seconds
- **Notes:**
  - Supports both testnet and production endpoints
  - Symbol format conversion: 'BTC/USDT' → 'BTCUSDT'
  - Retry logic not implemented (could improve reliability)

#### TelegramBot

- **Purpose:** Provides interactive user interface via Telegram
- **Location:** `trading_bot_bydfi.py` lines 229-621
- **Key Methods:**
  - `cmd_start()` - Welcome message
  - `cmd_help()` - Command reference
  - `cmd_menu()` - Interactive button menu
  - `cmd_balance()` - Show account balance
  - `cmd_price(symbol)` - Show current price
  - `cmd_analyze(symbol)` - Full technical analysis
  - `cmd_new_listings()` - Show new listings
  - `cmd_top_gainers()` - Show top gaining coins
  - `handle_text()` - Process plain text (coin symbols)
  - `button_callback()` - Handle inline button presses
  - `send_notification(message)` - Send push notification
- **Commands:**
  - `/start` - Initialization
  - `/help` - Help text
  - `/menu` - Interactive menu
  - `/balance` - Account balance
  - `/price SYMBOL` - Price query
  - `/analyze SYMBOL` - Technical analysis
  - `/listings` - New listings
  - `/top` - Top gainers
  - Plain text (e.g., "BTC") - Quick price check
- **Dependencies:**
  - Requires `TELEGRAM_BOT_TOKEN` environment variable
  - Requires `TELEGRAM_CHAT_ID` for notifications
  - Needs ByDFiExchange instance
- **Notes:**
  - Uses async/await for handlers
  - HTML parsing mode for formatted messages
  - Inline keyboard buttons for UX
  - Auto-formats symbols (BTC → BTCUSDT)

#### TradingBot

- **Purpose:** Main orchestrator - runs analysis loop and coordinates components
- **Location:** `trading_bot_bydfi.py` lines 624-789
- **Key Methods:**
  - `get_data()` - Fetch market data via ByDFiExchange
  - `calculate_indicators(df)` - Compute technical indicators
  - `analyze(df)` - Generate trading signal
  - `send_signal_notification(signal, metrics)` - Send Telegram alert
  - `run_analysis_loop(check_interval)` - Main analysis loop (default 1h)
  - `run()` - Start both Telegram bot and analysis loop
- **Analysis Logic:**
  - **BUY Signal**: RSI < 30 + MACD crossover up + bullish trend (EMA50 > EMA200)
  - **SELL Signal**: RSI > 70 + MACD crossover down + bearish trend (EMA50 < EMA200)
  - **HOLD**: Other conditions
  - Strong signals require all 3 conditions
  - Regular signals require 2/3 conditions
- **Configuration:**
  - Symbol: BTC/USDT (hardcoded, should be configurable)
  - Timeframe: 1h
  - RSI period: 14
  - RSI thresholds: 30 (oversold), 70 (overbought)
  - MACD: 12, 26, 9
  - EMA: 50, 200
  - Check interval: 3600s (1 hour)
- **Threading:**
  - Telegram bot runs in daemon thread
  - Analysis loop runs in main thread
- **Notes:**
  - Only sends notifications on signal changes
  - No persistence - restarts lose signal history
  - No trade execution - analysis only
  - Hardcoded to BTC/USDT (should be configurable)

---

## Testing Strategy

**Current Status:** ⚠️ No tests implemented yet

### Testing Levels

1. **Unit Tests** (Priority: High)
   - `ByDFiExchange._generate_signature()` - Test signature generation
   - `TradingBot.calculate_indicators()` - Test indicator calculations
   - `TradingBot.analyze()` - Test signal generation logic
   - Mock ByDFi API responses
   - Mock pandas DataFrames with known data

2. **Integration Tests** (Priority: Medium)
   - `ByDFiExchange` methods with testnet API
   - Telegram bot command handlers (mock bot API)
   - End-to-end data flow: API → analysis → signal

3. **End-to-End Tests** (Priority: Low)
   - Full bot workflow on testnet
   - Telegram bot interaction scenarios
   - Signal generation and notification delivery

### Test Implementation Recommendations

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Run tests
pytest tests/ -v --cov=src/

# Run with coverage report
pytest tests/ --cov=src/ --cov-report=html
```

### Writing Tests

**Example test structure:**

```python
import pytest
from unittest.mock import Mock, patch
from trading_bot_bydfi import ByDFiExchange, TradingBot

def test_signature_generation():
    """Test HMAC signature is generated correctly"""
    exchange = ByDFiExchange('test_key', 'test_secret', testnet=True)
    params = "symbol=BTCUSDT&timestamp=1234567890"
    signature = exchange._generate_signature(params)
    assert isinstance(signature, str)
    assert len(signature) == 64  # SHA256 hex length

@pytest.mark.asyncio
async def test_telegram_cmd_price(mock_exchange):
    """Test /price command returns formatted price"""
    # Test implementation
    pass
```

### Areas Requiring Tests

**Critical (must test):**
- API signature generation
- Technical indicator calculations
- Signal generation logic
- Error handling in API calls

**Important (should test):**
- Telegram command handlers
- Data parsing and formatting
- Symbol format conversion
- Balance calculation

**Nice to have:**
- Logging functionality
- Threading behavior
- Retry logic (when implemented)

### Test Coverage Goals

- **Target:** 80% overall coverage
- **Critical paths:** 95% coverage (signal generation, API auth)
- **UI handlers:** 60% coverage (Telegram commands)

---

## Deployment & CI/CD

**Current Status:** Manual deployment, no CI/CD pipeline

### Environments

- **Development:** Local machine with testnet
- **Testnet:** ByDFi testnet (api-cloud-testnet.bydfi.com)
- **Production:** ByDFi production (api-cloud.bydfi.com)

### Deployment Process

**Manual Deployment (Current):**

```bash
# 1. Clone repository
git clone <repository-url>
cd Trackerbot

# 2. Install system dependencies
sudo apt-get update
sudo apt-get install ta-lib python3-dev

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 6. Test on testnet first
# Set testnet=True in TradingBot.__init__()
python trading_bot_bydfi.py

# 7. Deploy to production
# Set testnet=False in TradingBot.__init__()
# Use process manager for persistence
nohup python trading_bot_bydfi.py > output.log 2>&1 &
# OR use systemd service (recommended)
```

**Recommended: Systemd Service**

```ini
# /etc/systemd/system/trackerbot.service
[Unit]
Description=Trackerbot Trading Bot
After=network.target

[Service]
Type=simple
User=tradingbot
WorkingDirectory=/opt/trackerbot
Environment="PATH=/opt/trackerbot/venv/bin"
ExecStart=/opt/trackerbot/venv/bin/python trading_bot_bydfi.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable trackerbot
sudo systemctl start trackerbot
sudo systemctl status trackerbot
```

### Recommended CI/CD Pipeline

**TODO: Implement GitHub Actions workflow**

```yaml
# .github/workflows/ci.yml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          sudo apt-get install ta-lib
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov
      - name: Lint
        run: flake8 src/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        # Add deployment steps
```

### Environment Variables

**Required environment variables in `.env` file:**

| Variable | Purpose | Required | Default | Example |
|----------|---------|----------|---------|---------|
| `BYDFI_API_KEY` | ByDFi API key | Yes | None | `abc123def456` |
| `BYDFI_API_SECRET` | ByDFi API secret | Yes | None | `xyz789uvw012` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Yes | None | `123456789:ABCdefGHI...` |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications | Yes | None | `987654321` |

**Important Security Notes:**
- **NEVER** commit `.env` file to git
- Add `.env` to `.gitignore`
- Use `.env.example` as template
- Rotate API keys periodically
- Use different keys for testnet and production
- Restrict API key permissions (read-only if not trading)

---

## Common Tasks

### Setting Up Development Environment

```bash
# 1. Clone repository
git clone <repository-url>
cd Trackerbot

# 2. Install system dependencies (TA-Lib)
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install ta-lib python3-dev build-essential

# macOS:
brew install ta-lib

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create environment configuration
cp .env.example .env
# Edit .env and add your credentials:
# BYDFI_API_KEY=your_key_here
# BYDFI_API_SECRET=your_secret_here
# TELEGRAM_BOT_TOKEN=your_bot_token_here
# TELEGRAM_CHAT_ID=your_chat_id_here

# 6. Get Telegram bot token
# - Message @BotFather on Telegram
# - Send /newbot and follow instructions
# - Copy token to .env

# 7. Get your Telegram chat ID
# - Message @userinfobot on Telegram
# - Copy your ID to .env

# 8. Get ByDFi API credentials
# - Register at https://www.bydfi.com/
# - Go to API Management
# - Create new API key (read-only for testing)
# - Copy key and secret to .env

# 9. Run in testnet mode (recommended for development)
# Edit trading_bot_bydfi.py line 638:
# testnet=True  (should already be True)

# 10. Run the bot
python trading_bot_bydfi.py

# 11. Test Telegram bot
# Send /start to your bot on Telegram
```

### Adding a New Feature

1. Create feature branch: `claude/[feature-name]-[session-id]`
2. Implement feature following conventions
3. Write tests for new functionality
4. Update documentation (including this file if needed)
5. Run test suite and linting
6. Commit changes with descriptive message
7. Push to remote
8. Create pull request

### Debugging

**Enable Debug Logging:**
```python
# In trading_bot_bydfi.py, change logging level:
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    # ... rest of config
)
```

**Check Logs:**
```bash
# View live logs
tail -f trading_bot_bydfi.log

# Search for errors
grep "ERROR" trading_bot_bydfi.log

# Search for specific symbol
grep "BTC" trading_bot_bydfi.log
```

**Test ByDFi API Connectivity:**
```python
# Quick test script
from trading_bot_bydfi import ByDFiExchange
import os
from dotenv import load_dotenv

load_dotenv()
exchange = ByDFiExchange(
    os.getenv('BYDFI_API_KEY'),
    os.getenv('BYDFI_API_SECRET'),
    testnet=True
)

# Test public endpoint
ticker = exchange.fetch_ticker('BTC/USDT')
print(ticker)

# Test authenticated endpoint
balance = exchange.fetch_balance()
print(balance)
```

**Test Telegram Bot:**
```bash
# Send test command to your bot
# /start
# /price BTCUSDT
# /help
```

**Common Debug Points:**
- API signature generation: Check timestamp and parameter sorting
- Telegram handlers: Verify async/await syntax
- Indicator calculation: Check for NaN values in DataFrame
- Symbol format: Ensure proper conversion (BTC/USDT ↔ BTCUSDT)

### API Testing

**Interactive ByDFi API Testing:**

```python
# Python REPL testing
python3
>>> from trading_bot_bydfi import ByDFiExchange
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>>
>>> exchange = ByDFiExchange(
...     os.getenv('BYDFI_API_KEY'),
...     os.getenv('BYDFI_API_SECRET'),
...     testnet=True
... )
>>>
>>> # Test endpoints
>>> exchange.fetch_ticker('BTC/USDT')
>>> exchange.fetch_ohlcv('BTC/USDT', '1h', 10)
>>> exchange.fetch_all_tickers()
>>> exchange.fetch_balance()
```

**Using curl to test ByDFi API:**

```bash
# Public endpoint (no auth)
curl "https://api-cloud-testnet.bydfi.com/spot/market/ticker?symbol=BTCUSDT"

# Authenticated endpoint requires signature
# Use the Python client instead
```

**Telegram Bot API Testing:**

```bash
# Get bot info
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"

# Send test message
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -d "chat_id=<YOUR_CHAT_ID>" \
  -d "text=Test message"
```

---

## Troubleshooting

### Common Issues

#### Issue: TA-Lib Installation Fails

**Symptoms:**
- `pip install TA-Lib` fails with compilation errors
- Error: "ta-lib/ta_libc.h: No such file or directory"

**Solution:**
```bash
# Install C library first
# Ubuntu/Debian:
sudo apt-get install ta-lib

# macOS:
brew install ta-lib

# If still fails, install from source:
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# Then install Python wrapper:
pip install TA-Lib
```

#### Issue: ByDFi API Returns Error Code

**Symptoms:**
- "Ошибка API ByDFi [code]: message"
- Common codes: 10001 (invalid signature), 10002 (invalid timestamp)

**Solution:**
```python
# Check timestamp is within recvWindow (5000ms)
# Verify system time is synchronized
sudo ntpdate -s time.nist.gov  # Linux
# Or
sudo sntp -sS time.windows.com  # macOS

# Verify signature generation:
# - Parameters must be sorted alphabetically
# - Use correct HMAC-SHA256 algorithm
# - Check API key and secret are correct
```

#### Issue: Telegram Bot Not Responding

**Symptoms:**
- Bot shows online but doesn't respond to commands
- No error in logs

**Solution:**
```bash
# 1. Check bot token is correct
# 2. Verify bot has permission to receive messages
# 3. Check if another instance is running:
ps aux | grep trading_bot_bydfi.py
# Kill duplicate processes if any

# 4. Test bot token:
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# 5. Check for rate limiting
# 6. Restart bot
```

#### Issue: "Not Enough Data" Error

**Symptoms:**
- "❌ Недостаточно данных для BTCUSDT"
- Analysis fails immediately

**Solution:**
- Ensure symbol has trading history
- Try a more popular pair (BTC/USDT, ETH/USDT)
- Increase limit in fetch_ohlcv() call
- Check if exchange is in maintenance mode
- Verify testnet vs production endpoint

#### Issue: Signal Generation Not Working

**Symptoms:**
- Bot runs but never generates signals
- Always returns "ДЕРЖАТЬ" (HOLD)

**Solution:**
```python
# 1. Check indicator calculations
df = bot.get_data()
df = bot.calculate_indicators(df)
print(df[['rsi', 'macd', 'macdsignal', 'ema_50', 'ema_200']].tail())

# 2. Verify no NaN values
print(df.isna().sum())

# 3. Check if conditions are too strict
# Consider adjusting thresholds in analyze() method

# 4. Test with known volatile period
# Use historical data with clear trends
```

#### Issue: High Memory Usage

**Symptoms:**
- Bot consumes increasing memory over time
- Eventually crashes or slows down

**Solution:**
- Limit DataFrame size in get_data() (current: 100 rows, good)
- Clear old signals_history periodically
- Add memory profiling:
```python
import tracemalloc
tracemalloc.start()
# ... your code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current/1024/1024:.2f}MB, Peak: {peak/1024/1024:.2f}MB")
```

#### Issue: Bot Stops After Some Time

**Symptoms:**
- Bot runs fine initially, then stops responding
- No obvious error in logs

**Solution:**
```bash
# 1. Use process manager (systemd recommended)
# 2. Add exception handling in main loop
# 3. Implement heartbeat monitoring
# 4. Check for network issues:
ping api-cloud-testnet.bydfi.com

# 5. Add connection retry logic
# 6. Monitor system resources (disk space, memory)
df -h
free -m
```

#### Issue: Incorrect Signature Error (403)

**Symptoms:**
- API returns "Invalid signature" or HTTP 403
- Authentication fails

**Solution:**
```python
# Debug signature generation:
1. Print params_str before signing
2. Verify parameter sorting is alphabetical
3. Check API secret has no extra spaces/newlines
4. Ensure timestamp is current (not cached)
5. Verify recvWindow is appropriate (5000ms default)

# Test with minimal request:
params = {'timestamp': int(time.time() * 1000)}
print(params)
# Should be recent Unix timestamp in milliseconds
```

---

## Important Notes for AI Assistants

### Critical Guidelines

1. **Read Before Writing**
   - ALWAYS read files before modifying them
   - Understand existing code before suggesting changes
   - Don't propose changes to code you haven't examined

2. **Avoid Over-Engineering**
   - Only make requested changes
   - Don't add unrequested features or "improvements"
   - Keep solutions simple and focused
   - Don't add error handling for impossible scenarios

3. **Security First**
   - Always check for OWASP Top 10 vulnerabilities
   - Validate at system boundaries only
   - Don't add unnecessary validation for internal code
   - If you write insecure code, fix it immediately

4. **Testing**
   - Run existing tests before making changes
   - Write tests for new functionality
   - Fix any tests broken by your changes
   - Don't commit if tests fail

5. **Documentation**
   - Update CLAUDE.md when architecture changes
   - Keep comments minimal and focused on "why"
   - Update README.md for user-facing changes
   - Document breaking changes clearly

6. **Git Operations**
   - All branches must follow naming convention
   - Always use descriptive commit messages
   - Never skip git hooks
   - Never force push to main/master
   - Retry pushes with exponential backoff on network errors

7. **Code Review Mindset**
   - Think about maintainability
   - Consider edge cases
   - Look for potential bugs
   - Ensure consistency with existing patterns

### Using This Document

1. **Start Here:** Always read this document before making significant changes
2. **Update As You Go:** If you discover outdated information, update it
3. **Add Context:** When you learn something important, document it
4. **Keep It Current:** This document is only valuable if maintained

### Critical Code Areas Requiring Extra Caution

**API Authentication (`ByDFiExchange._generate_signature`):**
- Signature algorithm is security-critical
- Must match ByDFi's exact requirements
- Test thoroughly before changing
- Any error will result in 403/authentication failure

**Signal Generation Logic (`TradingBot.analyze`):**
- Core business logic for trading decisions
- Changes directly impact trading recommendations
- Test with historical data before deploying
- Consider logging signal details for analysis

**Telegram Bot Handlers:**
- User-facing interface - clarity is critical
- Format messages for mobile readability
- Handle errors gracefully with user-friendly messages
- Consider rate limiting to prevent abuse

**Threading and Async:**
- Telegram bot uses async/await
- Analysis loop uses threading
- Be careful with shared state
- Avoid blocking operations in async handlers

**Error Handling in API Calls:**
- Currently returns None on errors (may hide issues)
- Consider more robust error handling:
  - Retry logic with exponential backoff
  - Circuit breaker pattern
  - Detailed error logging
  - User notifications for critical failures

### Task Management

- Use TodoWrite tool for complex multi-step tasks (3+ steps)
- Mark tasks in_progress before starting
- Mark tasks completed immediately after finishing
- Only mark completed when fully done (tests passing, no errors)
- One task in_progress at a time

### When Stuck

1. Read relevant source code carefully
2. Check this document for patterns and conventions
3. Look for similar implementations in the codebase
4. Ask user for clarification if requirements are unclear
5. Consult external documentation for frameworks/libraries

---

## Maintenance Checklist

Use this checklist when updating CLAUDE.md:

- [ ] Update "Last Updated" date at top
- [ ] Verify repository structure is current
- [ ] Update technology stack if changed
- [ ] Document new components or features
- [ ] Update common tasks if workflow changed
- [ ] Add new troubleshooting entries
- [ ] Remove outdated information
- [ ] Verify all code examples are correct
- [ ] Update architecture diagrams if needed
- [ ] Review and update testing strategy

---

## Additional Resources

### External Documentation

**ByDFi API:**
- Official API Documentation: https://bydfi-api-docs.com/ (check their website for current link)
- Testnet endpoint: https://api-cloud-testnet.bydfi.com
- Production endpoint: https://api-cloud.bydfi.com
- Note: API documentation may be limited - reverse engineer from similar exchanges if needed

**Telegram Bot API:**
- python-telegram-bot library: https://docs.python-telegram-bot.org/
- Telegram Bot API: https://core.telegram.org/bots/api
- BotFather commands: https://core.telegram.org/bots#6-botfather

**Technical Analysis (TA-Lib):**
- TA-Lib documentation: https://mrjbq7.github.io/ta-lib/
- Technical indicators explained: https://www.investopedia.com/technical-analysis-4689657
- TA-Lib installation: https://github.com/mrjbq7/ta-lib

**Python Libraries:**
- pandas: https://pandas.pydata.org/docs/
- requests: https://requests.readthedocs.io/
- python-dotenv: https://pypi.org/project/python-dotenv/

### Related Files

- `README.md` - User-facing project documentation (create if doesn't exist)
- `requirements.txt` - Python dependencies (create from code analysis)
- `.env.example` - Template for environment variables (should create)
- `.gitignore` - Git ignore patterns (should create to exclude .env, logs, etc.)

---

## Version History

| Version | Date | Changes | Updated By |
|---------|------|---------|------------|
| 1.0.0 | 2026-01-21 | Initial CLAUDE.md creation with template | Claude |
| 1.1.0 | 2026-01-21 | Comprehensive update based on actual codebase analysis | Claude |

---

**Remember:** This document exists to make AI assistants more effective at working on Trackerbot. Keep it updated, keep it accurate, and keep it useful.
