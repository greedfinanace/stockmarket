# Stock Tracker

A simple, yet powerful, stock tracker that runs directly in your terminal. This application fetches real-time stock data from multiple sources and displays it in a clean, easy-to-read format.

## Features

- **Multiple Data Sources:** Choose between Alpha Vantage and Yahoo Finance (`yfinance`) for your stock data.
- **Real-Time Data:** Get the latest stock information, including open, high, low, close, and volume.
- **Interactive CLI:** An easy-to-use command-line interface for entering stock symbols.
- **Beautiful Output:** Clean, formatted table output using the `rich` library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.6 or higher
- An API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) (only required if using Alpha Vantage as a data source)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/greedfinanace/stockmarket.git
   cd stockmarket
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables (for Alpha Vantage):**

   If you plan to use Alpha Vantage, create a new file named `.env` in the root of the project and add your API key:

   ```
   ALPHA_VANTAGE_API_KEY=YOUR_API_KEY
   ```

   Replace `YOUR_API_KEY` with your actual Alpha Vantage API key.

## Usage

To run the application, execute the `stock_tracker.py` script:

```bash
python stock_tracker.py
```

You will first be prompted to select your data source (Alpha Vantage or Yahoo Finance). After selecting a source, you can enter any stock symbol (e.g., `AAPL`, `MSFT`) to get the latest data.
