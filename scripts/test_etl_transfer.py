import unittest
from unittest.mock import patch, MagicMock
from etl_transfer import new_func

class TestNewFunc(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_new_func_calls_psycopg2_connect_with_correct_args(self, mock_connect):
        # Arrange
        SRC_DB = "test_db"
        USER = "test_user"
        PW = "test_pw"
        HOST = "localhost"
        PORT = "5432"
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Act
        result = new_func(SRC_DB, USER, PW, HOST, PORT)

        # Assert
        mock_connect.assert_called_once_with(
            dbname=SRC_DB, user=USER, password=PW, host=HOST, port=PORT
        )
        self.assertEqual(result, mock_conn)

    @patch("psycopg2.connect", side_effect=Exception("Connection failed"))
    def test_new_func_raises_exception_on_connection_error(self, mock_connect):
        with self.assertRaises(Exception) as context:
            new_func("db", "user", "pw", "host", "port")
        self.assertIn("Connection failed", str(context.exception))

if __name__ == "__main__":
    unittest.main()