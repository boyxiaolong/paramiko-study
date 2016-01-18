#-*- coding: utf-8 -*-
import unittest
from pycrypo_connector import Connector
import ConfigParser

class TestConn(unittest.TestCase):
    def setUp(self):
        self.test = Connector('192.168.2.161', 22, 'tianqi', 'tianqi', 1)
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

config = ConfigParser.ConfigParser()
config.read("config.ini")

if __name__ == '__main__':
    #unittest.main()
    test = Connector(config.get('host2', 'host'), config.get('host2', 'port'), config.get('host2', 'usrname'), config.get('host2', 'pwd'), 1)
    test.connect()
    test.get_logger().debug("end connect")
    #test.run_command_interactive_async()
