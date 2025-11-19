import os
import requests
import yfinance as yf
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
import asciichartpy

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Initialize Rich console
console = Console()

def get_alphavantage_data(symbol):
    """
    Fetches stock data for a given symbol from the Alpha Vantage API.
    Returns a dictionary containing the latest data and historical close prices.
    """
    if not API_KEY:
        console.print("[bold red]Error: ALPHA_VANTAGE_API_KEY not found in .env file.[/bold red]")
        return None

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=15min&outputsize=compact&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            console.print(f"[bold red]API Error: {data['Error Message']}[/bold red]")
            return None

        time_series = data.get("Time Series (15min)")
        if not time_series:
            console.print(f"[bold yellow]No time series data found for {symbol.upper()}[/bold yellow]")
            return None

        # Sort timestamps and get the latest
        sorted_timestamps = sorted(time_series.keys(), reverse=True)
        latest_timestamp = sorted_timestamps[0]
        latest_data = time_series[latest_timestamp]

        # Get historical data for the chart (reversed to be in chronological order)
        historical_closes = [float(time_series[ts]['4. close']) for ts in reversed(sorted_timestamps)]

        return {
            "latest": {
                "timestamp": latest_timestamp,
                "open": latest_data.get("1. open"),
                "high": latest_data.get("2. high"),
                "low": latest_data.get("3. low"),
                "close": latest_data.get("4. close"),
                "volume": latest_data.get("5. volume")
            },
            "history": historical_closes
        }

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching data from Alpha Vantage: {e}[/bold red]")
        return None
    except (KeyError, IndexError):
        console.print(f"[bold red]Could not parse Alpha Vantage data for {symbol.upper()}[/bold red]")
        return None

def get_yfinance_data(symbol):
    """
    Fetches stock data for a given symbol from Yahoo Finance.
    Returns a dictionary containing the latest data and historical close prices.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="15m")
        if hist.empty:
            console.print(f"[bold yellow]No data found for symbol: {symbol.upper()} using yfinance.[/bold yellow]")
            return None

        latest_data = hist.iloc[-1]
        historical_closes = hist['Close'].tolist()

        return {
            "latest": {
                "timestamp": latest_data.name.strftime('%Y-%m-%d %H:%M:%S'),
                "open": f"{latest_data['Open']:.4f}",
                "high": f"{latest_data['High']:.4f}",
                "low": f"{latest_data['Low']:.4f}",
                "close": f"{latest_data['Close']:.4f}",
                "volume": str(latest_data['Volume'])
            },
            "history": historical_closes
        }
    except Exception as e:
        console.print(f"[bold red]Error fetching data from yfinance for {symbol.upper()}: {e}[/bold red]")
        return None

def display_stock_data(data, symbol, source):
    """
    Displays the stock data in a formatted table.
    """
    if not data:
        return

    table = Table(title=f"Stock Data for {symbol.upper()} (Source: {source})", show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Latest Timestamp", data.get("timestamp", "N/A"))
    table.add_row("Open", data.get("open", "N/A"))
    table.add_row("High", data.get("high", "N/A"))
    table.add_row("Low", data.get("low", "N/A"))
    table.add_row("Close", data.get("close", "N/A"))
    table.add_row("Volume", data.get("volume", "N/A"))

    console.print(table)

def display_price_chart(historical_data):
    """
    Displays a price chart using asciichartpy.
    """
    if not historical_data:
        return

    # Configuration for the chart
    config = {
        'height': 15,
        'format': '{:8.2f} '
    }

    chart = asciichartpy.plot(historical_data, config)
    console.print("\n[bold green]Recent Price Trend:[/bold green]")
    console.print(chart)

def main():
    """
    Main function to run the stock tracker application.
    """
    source = ""
    while not source:
        choice = console.input("[bold cyan]Select data source (1 for Alpha Vantage, 2 for Yahoo Finance): [/bold cyan]").strip()
        if choice == '1':
            source = "Alpha Vantage"
        elif choice == '2':
            source = "Yahoo Finance"
        else:
            console.print("[bold red]Invalid choice. Please enter 1 or 2.[/bold red]")

    get_data_func = get_alphavantage_data if source == "Alpha Vantage" else get_yfinance_data

    while True:
        symbol = console.input("[bold cyan]Enter a stock symbol (e.g., AAPL, MSFT) or type 'exit' to quit: [/bold cyan]").upper().strip()
        if symbol == 'EXIT':
            break
        if not symbol:
            console.print("[bold red]Please enter a stock symbol.[/bold red]")
            continue

        data_package = get_data_func(symbol)
        if data_package:
            display_stock_data(data_package["latest"], symbol, source)
            display_price_chart(data_package["history"])

if __name__ == "__main__":
    main()
