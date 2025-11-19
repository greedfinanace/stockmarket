import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from stock_tracker import get_alphavantage_data, get_yfinance_data, display_stock_data, display_price_chart, main

class TestStockTracker(unittest.TestCase):

    @patch('stock_tracker.API_KEY', 'DUMMY_KEY')
    @patch('stock_tracker.requests.get')
    def test_get_alphavantage_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Time Series (15min)": {
                "2024-01-01 10:00:00": {
                    "1. open": "150.00", "2. high": "151.00", "3. low": "149.00",
                    "4. close": "150.50", "5. volume": "100000"
                }
            }
        }
        mock_get.return_value = mock_response
        data = get_alphavantage_data("AAPL")
        self.assertIsNotNone(data)
        self.assertEqual(data['latest']['open'], "150.00")
        self.assertIsInstance(data['history'], list)

    @patch('yfinance.Ticker')
    def test_get_yfinance_data_success(self, mock_ticker):
        # Create a mock DataFrame
        mock_df = pd.DataFrame({
            'Open': [150.0], 'High': [151.0], 'Low': [149.0],
            'Close': [150.5], 'Volume': [100000]
        }, index=[pd.to_datetime("2024-01-01 10:00:00")])

        mock_instance = mock_ticker.return_value
        mock_instance.history.return_value = mock_df

        data = get_yfinance_data("AAPL")
        self.assertIsNotNone(data)
        self.assertEqual(data['latest']['open'], "150.0000")
        self.assertIsInstance(data['history'], list)

    @patch('stock_tracker.console.print')
    def test_display_stock_data(self, mock_print):
        data = {"open": "150.00"}
        display_stock_data(data, "AAPL", "Test Source")
        self.assertTrue(mock_print.called)

    @patch('asciichartpy.plot')
    @patch('stock_tracker.console.print')
    def test_display_price_chart(self, mock_print, mock_plot):
        display_price_chart([1, 2, 3])
        mock_plot.assert_called_once()
        self.assertTrue(mock_print.called)

    @patch('stock_tracker.console.input', side_effect=['1', 'AAPL', 'exit'])
    @patch('stock_tracker.get_alphavantage_data')
    @patch('stock_tracker.display_price_chart')
    def test_main_alpha_vantage_flow(self, mock_display_chart, mock_get_data, mock_input):
        mock_get_data.return_value = {"latest": {"open": "150.00"}, "history": [150.50]}
        main()
        mock_get_data.assert_called_with("AAPL")
        mock_display_chart.assert_called_with([150.50])

    @patch('stock_tracker.console.input', side_effect=['2', 'MSFT', 'exit'])
    @patch('stock_tracker.get_yfinance_data')
    @patch('stock_tracker.display_price_chart')
    def test_main_yfinance_flow(self, mock_display_chart, mock_get_data, mock_input):
        mock_get_data.return_value = {"latest": {"open": "300.00"}, "history": [300.00]}
        main()
        mock_get_data.assert_called_with("MSFT")
        mock_display_chart.assert_called_with([300.00])

if __name__ == '__main__':
    unittest.main()
