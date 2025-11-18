# Stock Tracker

A simple, yet powerful, stock tracker that runs directly in your terminal. This application fetches real-time stock data from the Alpha Vantage API and displays it in a clean, easy-to-read format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- An API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/stock-tracker.git
   cd stock-tracker
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

4. **Set up your environment variables:**

   - Create a new file named `.env` in the root of the project.
   - Add your Alpha Vantage API key to the `.env` file as follows:

     ```
     ALPHA_VANTAGE_API_KEY=YOUR_API_KEY
     ```

     Replace `YOUR_API_KEY` with your actual Alpha Vantage API key.

## Usage

To run the application, simply execute the `stock_tracker.py` script:

```bash
python stock_tracker.py
```

You will be prompted to enter a stock symbol (e.g., `AAPL`, `MSFT`). The application will then fetch and display the latest stock data for that symbol.
