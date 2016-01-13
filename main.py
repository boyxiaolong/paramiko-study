#-*- coding: utf-8 -*-
from pycrypoConnector import Connector

def main():
    test = Connector('192.168.2.161', 22, 'tianqi', 'tianqi')
    test.connect()
    test.run_command("ls")
    test.run_command('cat /proc/meminfo')

if __name__ == '__main__':
    main()
