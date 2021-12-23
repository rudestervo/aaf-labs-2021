import unittest
from parser import Parser
from unittest.mock import patch

class MyTestCase(unittest.TestCase):
    string_input = 'create cats (id indexed, name, value); exit;'
    @patch('builtins.input', return_value=string_input)
    def test_something(self, mock_input):
        result = Parser()
        assertError


if __name__ == '__main__':
    unittest.main()
