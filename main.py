#-*- coding: utf-8 -*-
import unittest
from pycrypo_connector import Connector

class TestConn(unittest.TestCase):
    def setUp(self):
        self.test = Connector('192.168.3.105', 22, 'allen', '123')
        self.assertTrue(self.test.connect())
    def tearDown(self):
        print 'teardowo'
    def test_single_cmd(self):
        self.test.run_command_interactive_syc('ls')
        self.test.run_command_immediate('cat /proc/meminfo')
    def test_interactive_cmd(self):
        self.test.run_command_interactive_syc(['su\n', 'root\n', 'whoami'])
    def test_1(self):
        self.test.run_command_interactive_async()

if __name__ == '__main__':
    unittest.main()
