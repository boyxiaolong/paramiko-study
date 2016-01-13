#-*- coding: utf-8 -*-

import paramiko

class Test:
    host = '192.168.2.161'
    username = 'tianqi'
    password = 'tianqi'
    connector = None

    def __init__(self):
        paramiko.util.log_to_file('paramiko_util.log')
    def connect(self):
        """
        Connect to the device
        """
        try:
            self.connector = paramiko.SSHClient()
            self.connector.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.connector.connect(
                hostname=self.host,
                username=self.username,
                password=self.password)

            print 'connect success to',self.host
        except Exception as e:
            raise Exception(("Connection Failed"))
    def run_command(self, cmd_str):
        if self.connector:
            try:
                stdin, stdout, stderr = self.connector.exec_command(cmd_str)
                for line in stdout:
                    print '..'+line.strip('\n')
            except paramiko.SSHException as e:
                print e

    def close(self):
        if self.connector:
            self.connector.close()

test = Test()
test.connect()
test.run_command("free -m")
test.close()
