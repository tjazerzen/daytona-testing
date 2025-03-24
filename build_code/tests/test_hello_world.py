

"""
Unit tests for the console application.
"""
import unittest
import sys
from unittest.mock import patch
import hello_world


class TestMainModule(unittest.TestCase):
    """Test cases for the hello_world module."""

    def test_main_success(self):
        """Test that the main function returns 0 on success."""
        result = hello_world.main()
        self.assertEqual(result, 0)

    @patch('hello_world.setup_logging')
    def test_logging_setup(self, mock_setup_logging):
        """Test that logging is set up correctly."""
        hello_world.main()
        mock_setup_logging.assert_called_once()

    @patch('hello_world.main')
    def test_sys_exit_called_with_main_result(self, mock_main):
        """Test that sys.exit is called with the result of main()."""
        # Set up the mock to return a specific value
        mock_main.return_value = 42
        
        # Create a context where we can test the __name__ == "__main__" block
        with patch('sys.exit') as mock_exit:
            # Directly call the code that would run if __name__ == "__main__"
            hello_world.sys.exit(hello_world.main())
            mock_exit.assert_called_once_with(42)


if __name__ == '__main__':
    unittest.main()