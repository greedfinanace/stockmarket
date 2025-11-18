import unittest
from unittest.mock import patch, MagicMock
from stock_tracker import get_stock_data, display_stock_data

class TestStockTracker(unittest.TestCase):

    @patch('stock_tracker.API_KEY', 'DUMMY_KEY')
    @patch('stock_tracker.requests.get')
    def test_get_stock_data_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Time Series (5min)": {
                "2024-01-01 10:00:00": {
                    "1. open": "150.00",
                    "2. high": "151.00",
                    "3. low": "149.00",
                    "4. close": "150.50",
                    "5. volume": "100000"
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function
        data = get_stock_data("AAPL")

        # Assertions
        self.assertIsNotNone(data)
        self.assertIn("Time Series (5min)", data)

    @patch('stock_tracker.API_KEY', 'DUMMY_KEY')
    @patch('stock_tracker.requests.get')
    def test_get_stock_data_api_error(self, mock_get):
        # Mock the API response for an error
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Error Message": "Invalid API Key"}
        mock_get.return_value = mock_response

        # Call the function
        data = get_stock_data("AAPL")

        # Assertions
        self.assertIsNone(data)

    @patch('stock_tracker.console.print')
    def test_display_stock_data(self, mock_print):
        # Mock data
        data = {
            "Time Series (5min)": {
                "2024-01-01 10:00:00": {
                    "1. open": "150.00",
                    "2. high": "151.00",
                    "3. low": "149.00",
                    "4. close": "150.50",
                    "5. volume": "100000"
                }
            }
        }

        # Call the function
        display_stock_data(data, "AAPL")

        # Assertions
        self.assertTrue(mock_print.called)

    @patch('stock_tracker.API_KEY', None)
    @patch('stock_tracker.console.print')
    def test_get_stock_data_no_api_key(self, mock_print):
        # Call the function
        data = get_stock_data("AAPL")

        # Assertions
        self.assertIsNone(data)
        mock_print.assert_called_with("[bold red]Error: ALPHA_VANTAGE_API_KEY not found in .env file.[/bold red]")

if __name__ == '__main__':
    unittest.main()
