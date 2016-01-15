#-*- coding: utf-8 -*-
import socket
import logging
import paramiko
from bcolors import bcolor
import interactive

class Connector(object):
    """
    Connector for paramiko client
    """

    def __init__(self, host, port, username, pwd, timeout):
        self.host = host
        self.port = port
        self.username = username
        self.password = pwd
        self.shell = None
        self.timeout = timeout
        self.connector = paramiko.SSHClient()
        paramiko.util.log_to_file('paramiko_util.log')
        self.logger = logging.getLogger("paramiko")

    def connect(self):
        """
        Connect to the device
        """
        try:
            #if first connect to server the key is empty, and load next time
            self.connector.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #self.connector.load_system_host_keys()
            self.connector.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                timeout=self.timeout)
            self.logger = self.connector.get_transport().logger
            self.logger.debug("connect success logic")
            return True
        except paramiko.BadHostKeyException as e:
            print 'BadHostKeyException'
            return False
        except paramiko.AuthenticationException as e:
            print 'AuthenticationException'
            return False
        except paramiko.SSHException as e:
            print e
            return False
        except socket.error as e:
            print e
            return False

    def run_command_immediate(self, cmd_str):
        if self.connector:
            try:
                stdin, stdout, stderr = self.connector.exec_command(cmd_str)
                print bcolor.HEADER, 'the cmd: ',cmd_str," result is:"
                for line in stdout:
                    print bcolor.OKGREEN, line.strip('\n')
                print '\n'
            except paramiko.SSHException as e:
                print e

    def run_command_interactive_syc(self, cmd_list):
        if self.connector:
            if not self.shell:
                self.shell = self.connector.invoke_shell()
            for cmd in cmd_list:
                print 'cmd ', cmd
                self.shell.send(cmd)
                receive_buf = self.shell.recv(1024)
                print receive_buf
    def run_command_interactive_async(self):
        if not self.shell:
            self.shell = self.connector.invoke_shell()
        interactive.interactive_shell(self.shell)
        return
    def __del__(self):
        if self.shell:
            self.shell.close()
        if self.connector:
            self.connector.close()

    def get_logger(self):
        return self.logger
