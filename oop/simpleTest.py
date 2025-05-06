import unittest
from unittest.mock import patch
from simpleClass import Worker  # Replace 'worker_module' with the actual module name

class TestWorker(unittest.TestCase):

    def setUp(self):
        self.worker = Worker(name="Steve", is_working=True, num_reprimands=0)

    @patch('builtins.print')
    def test_hide_from_boss(self, mock_print):
        self.worker.hide_from_boss()
        mock_print.assert_called_once_with("Steve is hiding from the boss.")
        self.assertEqual(self.worker.num_reprimands, 1)

    @patch('builtins.print')
    def test_act_like_working(self, mock_print):
        self.worker.act_like_working()
        mock_print.assert_called_once_with("Steve is pretending to work.")
        self.assertFalse(self.worker.is_working)

if __name__ == "__main__":
    unittest.main()
