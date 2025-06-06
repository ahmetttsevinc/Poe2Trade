# Path of Exile 2 Currency Arbitrage Tool

🚧 **UNDER CONSTRUCTION - WAITING FOR OFFICIAL API** 🚧

This project is currently on hold, waiting for Grinding Gear Games to release official APIs for Path of Exile 2 trading. Once the official APIs become available, development will resume.

A currency arbitrage analysis tool for Path of Exile 2 that identifies profitable currency exchange opportunities using market data from official APIs.

**IMPORTANT DISCLAIMER: This product isn't affiliated with or endorsed by Grinding Gear Games in any way.**

## Current Status

⚠️ **Not Currently Functional** ⚠️

The tool is waiting for:

- Official Path of Exile 2 Trading APIs
- Public API documentation from Grinding Gear Games
- Official trading endpoints and authentication methods

Development will resume once these requirements are met.

## Planned Features

- Live market data analysis from official APIs
- Automated detection of currency arbitrage opportunities
- Advanced arbitrage detection using Bellman-Ford algorithm
- Real-time exchange rate monitoring
- Configurable profit margin thresholds
- Comprehensive logging system
- Multiple currency pair analysis
- Easy exit mechanism

## Prerequisites

- Python 3.8 or higher
- Required packages listed in requirements.txt

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Future Implementation

The tool is designed to use official APIs for:

- Market data retrieval
- Currency exchange rate analysis
- Price monitoring
- User authentication

These features will be implemented once the official APIs are available.

## Configuration

The tool comes with default settings that can be modified in `poe2_currency_arbitrage.py`:

- `analysis_cooldown`: Time between market analyses (default: 5 seconds)
- `min_profit_margin`: Minimum profit required for opportunity detection (default: 10%)
- Logging configuration can be adjusted in the logging setup section

## Usage

1. Run the tool:

```bash
python poe2_currency_arbitrage.py
```

2. The tool will:

   - Connect to the official APIs and fetch market data
   - Monitor currency exchange rates
   - Calculate potential arbitrage opportunities
   - Log all findings and analyses
   - Display profitable opportunities when found

3. Press `ESC` at any time to safely stop the tool

## Data Management

- The tool fetches market data from official APIs
- Data is temporarily cached to prevent excessive requests
- Cache is automatically refreshed every 5 minutes
- Market data is stored in `market_data.json`

## Logging

All tool activities are logged to `arbitrage.log`, including:

- Market data updates
- Found arbitrage opportunities
- Analysis results
- Errors and warnings

## Safety Features

- Rate limiting for API requests
- Error handling for failed requests
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
