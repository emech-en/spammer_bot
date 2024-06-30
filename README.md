# Telegram Spam Filter Bot

[فارسی](README_FA.md) | English

This is an intelligent spam filter bot for Telegram, built using artificial intelligence. The bot is capable of
detecting and filtering spam messages in Telegram groups.

## About the Creator

Hello! I'm Claude, an advanced AI created by Anthropic. I assisted in creating this spam filter bot and can help with a
wide range of tasks including programming, data analysis, writing, and much more. While I'm an AI, I strive to provide
accurate, helpful, and ethical responses.

This project is an example of my capabilities in programming and system design. I can help you develop, improve, and
maintain this bot or similar projects. If you have any questions or need further assistance, I'd be happy to help!

## Features

- Detection and removal of spam messages
- Limitation on the number of personal and forwarded messages
- Sending warnings to spammer users
- Ability to configure parameters through environment variables

## Requirements

- Python 3.9+
- python-telegram-bot 20.3+
- Docker (optional)

## How to Use

### Method 1: Direct Execution

1. Clone the repository:
   ```
   git clone https://github.com/emech-en/spammer_bot.git
   cd spammer_bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file and set the environment variables:
   ```
   BOT_TOKEN=your_bot_token_here
   PERSONAL_MAX_PER_MINUTE=5
   FORWARD_MAX_PER_HOUR=1
   FORWARD_MAX_PER_FIVE_HOURS=3
   WARNING_COOLDOWN=3600
   ```

4. Run the bot:
   ```
   python spammer_bot.py
   ```

### Method 2: Using Docker

1. Clone the repository:
   ```
   git clone https://github.com/emech-en/spammer_bot.git
   cd spammer_bot
   ```

2. Create and set up the `.env` file as shown above.

3. Build and run the Docker image:
   ```
   docker-compose up --build
   ```

## Configuration

You can configure the following parameters through environment variables:

- `BOT_TOKEN`: Your Telegram bot token
- `PERSONAL_MAX_PER_MINUTE`: Maximum number of personal messages allowed per minute
- `FORWARD_MAX_PER_HOUR`: Maximum number of forwarded messages allowed per hour
- `FORWARD_MAX_PER_FIVE_HOURS`: Maximum number of forwarded messages allowed per 5 hours
- `WARNING_COOLDOWN`: Waiting time between warnings (in seconds)

## Contributing

Contributions to this project are very welcome! Please open an issue first to discuss any major changes you'd like to
make.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.
