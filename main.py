#-*- coding: utf-8 -*-

from pycrypo_connector import Connector

def test_conn():
    test = Connector('192.168.2.161', 22, 'tianqi', 'tianqi')
    test.connect()
    test.run_command_immediate("ls")
    test.run_command_immediate('cat /proc/meminfo')
    test.run_command_interactive(['su\n', 'root\n', 'whoami'])

if __name__ == '__main__':
    test_conn()
