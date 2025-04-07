# Path of Exile 2 Trade Bot

An automated trading bot for Path of Exile 2 that finds and executes profitable currency arbitrage opportunities using live market data from the official trade site.

**IMPORTANT DISCLAIMER: This product isn't affiliated with or endorsed by Grinding Gear Games in any way.**

## Features

- Live market data fetching from official trade site
- Automated detection of profitable trading opportunities
- Currency arbitrage detection using Bellman-Ford algorithm
- Real-time price monitoring
- Configurable profit margins
- Comprehensive logging system
- Safe trade execution with cooldown periods
- Easy exit mechanism

## Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- ChromeDriver (will be automatically managed)

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The bot comes with default settings that can be modified in `cursortradebot.py`:

- `trade_cooldown`: Time between trades (default: 5 seconds)
- `min_profit_margin`: Minimum profit required for trade execution (default: 10%)
- Logging configuration can be adjusted in the logging setup section

## Usage

1. Run the bot:

```bash
python cursortradebot.py
```

2. The bot will:

   - Connect to the official trade site and fetch live market data
   - Monitor buy and sell prices for all currencies
   - Calculate profitable arbitrage opportunities
   - Execute trades when profitable opportunities are found
   - Log all activities to `tradebot.log`

3. Press `ESC` at any time to safely stop the bot

## Data Management

- The bot fetches live market data from the official trade site
- Data is temporarily cached to prevent excessive requests
- Cache is automatically refreshed every 5 minutes
- Backup data is stored in `temp_market_data.json`

## Logging

All bot activities are logged to `tradebot.log`, including:

- Market data updates
- Found trading opportunities
- Trade execution attempts and results
- Errors and warnings

## Safety Features

- Cooldown period between trades to prevent spam
- Error handling for failed trades
- Safe exit mechanism
- Comprehensive logging for monitoring
- Automatic data backup
- Connection error handling

## Legal Disclaimer

This software is provided for educational purposes only. Users are responsible for ensuring their use of this software complies with:

- Path of Exile's Terms of Service
- Trading guidelines and rules
- Local laws and regulations

**IMPORTANT:**

- This product isn't affiliated with or endorsed by Grinding Gear Games in any way.
- Path of Exile and Path of Exile 2 are registered trademarks of Grinding Gear Games.
- Use this software at your own risk.
- The developers are not responsible for any consequences of using this software.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License with additional restrictions - see the LICENSE file for details.

Note: This license does not grant any rights to use Grinding Gear Games' trademarks or other intellectual property. Path of Exile and Path of Exile 2 are registered trademarks of Grinding Gear Games.
