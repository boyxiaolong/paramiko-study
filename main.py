#-*- coding: utf-8 -*-
import unittest
from pycrypo_connector import Connector

class TestConn(unittest.TestCase):
    def setUp(self):
        self.test = Connector('192.168.2.161', 22, 'tianqi', 'tianqi')
        self.assertTrue(self.test.connect())
    def tearDown(self):
        print 'teardowo'
    def test_single_cmd(self):
        self.test.run_command_interactive('ls')
        self.test.run_command_immediate('cat /proc/meminfo')
    def test_interactive_cmd(self):
        self.test.run_command_interactive(['su\n', 'root\n', 'whoami'])


if __name__ == '__main__':
    unittest.main()
