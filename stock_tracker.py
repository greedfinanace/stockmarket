import os
import requests
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Initialize Rich console
console = Console()

def get_stock_data(symbol):
    """
    Fetches stock data for a given symbol from the Alpha Vantage API.
    """
    if not API_KEY:
        console.print("[bold red]Error: ALPHA_VANTAGE_API_KEY not found in .env file.[/bold red]")
        return None

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if "Error Message" in data:
            console.print(f"[bold red]Error: {data['Error Message']}[/bold red]")
            return None
        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching data: {e}[/bold red]")
        return None

def display_stock_data(data, symbol):
    """
    Displays the stock data in a formatted table.
    """
    if not data or "Time Series (5min)" not in data:
        console.print(f"[bold yellow]No data found for symbol: {symbol}[/bold yellow]")
        return

    # Get the most recent data point
    latest_timestamp = list(data["Time Series (5min)"].keys())[0]
    latest_data = data["Time Series (5min)"][latest_timestamp]

    # Create a table to display the data
    table = Table(title=f"Stock Data for {symbol.upper()}", show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    # Add rows to the table
    table.add_row("Latest Timestamp", latest_timestamp)
    table.add_row("Open", latest_data["1. open"])
    table.add_row("High", latest_data["2. high"])
    table.add_row("Low", latest_data["3. low"])
    table.add_row("Close", latest_data["4. close"])
    table.add_row("Volume", latest_data["5. volume"])

    # Print the table
    console.print(table)

if __name__ == "__main__":
    symbol = console.input("[bold cyan]Enter a stock symbol (e.g., AAPL, MSFT): [/bold cyan]").upper()
    if symbol:
        stock_data = get_stock_data(symbol)
        if stock_data:
            display_stock_data(stock_data, symbol)
