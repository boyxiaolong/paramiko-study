#-*- coding: utf-8 -*-
import socket
import paramiko
import logging
from bcolors import bcolor

class Connector:
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.password = pwd
        paramiko.util.log_to_file('paramiko_util.log')
    def connect(self):
        """
        Connect to the device
        """
        try:
            self.connector = paramiko.SSHClient()
            #if first connect to server the key is empty, and load next time
            self.connector.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connector.load_system_host_keys()
            self.connector.connect(
                hostname=self.host,
                username=self.username,
                password=self.password)

            print 'connect success to',self.host
        except paramiko.BadHostKeyException as e:
            print 'BadHostKeyException'
        except paramiko.AuthenticationException as e:
            print 'AuthenticationException'
        except paramiko.SSHException as e:
            print e
        except socket.error as e:
            print e

    def run_command(self, cmd_str):
        if self.connector:
            try:
                stdin, stdout, stderr = self.connector.exec_command(cmd_str)
                print bcolor.HEADER, 'the cmd: ',cmd_str," result is:"
                for line in stdout:
                    print bcolor.OKGREEN, line.strip('\n')
                print '\n'
            except paramiko.SSHException as e:
                print e

    def __del__(self):
        if self.connector:
            self.connector.close()
