# AGENTS.md - CanuckBot Development Guide

## Build & Test Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Lint with ruff
ruff check .
ruff format .

# Run bot locally
python bot.py

# Test specific cog
python -m pytest tests/test_cogs.py::test_competitions -v
```

## Code Style Guidelines
- **Imports**: Standard lib → 3rd party → local, absolute imports preferred
- **Types**: Use type hints everywhere, Pydantic for data models
- **Naming**: snake_case for vars/functions, PascalCase for classes, UPPER_SNAKE for constants
- **Error Handling**: Use try/except with specific exceptions, log with Discord.WebhookLoggerAdapter
- **Formatting**: 4-space tabs, 88 char line limit (ruff default)
- **Async**: All Discord operations must be async/await
- **Database**: Use aiosqlite with context managers, SQL in database/*.sql files