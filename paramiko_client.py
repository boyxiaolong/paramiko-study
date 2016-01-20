import paramiko
import ConfigParser

class ParamikoClient(object):
    def __init__(self, ini_file):
        config = ConfigParser.ConfigParser()
        pre_str = 'ssh1'
        config.read(ini_file)
        self.host = config.get(pre_str, 'host')
        self.port = config.getint(pre_str, 'port')
        self.usr = config.get(pre_str, 'usr')
        self.pwd = config.get(pre_str, 'pwd')
        self.timeout = config.getfloat(pre_str, 'timeout')

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.host, port=self.port, username=self.usr, password=self.pwd, timeout=self.timeout)
            return True
        except Exception,e:
            print 'caught ', e
            try:
                self.client.close()
                return False
            except:
                pass

    def run_command(self, cmd_str):
        stdin, stdout, stderr = self.client.exec_command(cmd_str)
        for line in stdout:
            print line

    def get_naive_client(self):
        return self.client