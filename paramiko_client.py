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
        self.sftp_client = None
        self.is_connected = False
        self.shell = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.host, port=self.port, username=self.usr, password=self.pwd, timeout=self.timeout)
            self.is_connected = True
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

    def run_multi_seq_command(self, cmd_list):
        if not self.shell:
            self.shell = self.client.invoke_shell()

        for cmd in cmd_list:
            self.shell.send(cmd+'\n')
            receive_buf = self.shell.recv(1024)
            print receive_buf
    def get_sftp_client(self):
        if self.is_connected == False:
            self.connect()
        if not self.sftp_client:
            self.sftp_client = paramiko.SFTPClient.from_transport(self.client.get_transport())
        return self.sftp_client

    def upload_file(self, local_file, remote_file):
        self.get_sftp_client().put(local_file, remote_file)

