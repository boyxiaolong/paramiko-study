import os
import time
from multiprocessing import Process, Pool
import paramiko
from paramiko_client import ParamikoClient
import gevent
import ConfigParser

def func():
    client = ParamikoClient('config.ini')
    print client.connect()
    client.run_command('date')

def multi_process_test():
    pool = Pool()
    results = []
    for i in range(3):
        results.append(pool.apply_async(func))
    pool.close()
    pool.join()

def test_gevent():
    gevent.joinall([
    gevent.spawn(func),
    gevent.spawn(func),])

last_total_req = 0
files = {}

def load_total():
    print 'todo'

def test_get():
    load_total()
    client = ParamikoClient('config.ini')
    print client.connect()
    sftp = paramiko.SFTPClient.from_transport(client.client.get_transport())
    remote_pre = '/home/tianqi/hailong/test/'
    local_pre = '/Users/allen/code/paramiko-study-1/'
    sftp.get(remote_pre+'total.txt', local_pre+'total.txt')
    config = ConfigParser.ConfigParser()
    config.read('total.txt')
    total_seq = config.getint('total', 'total_seq')
    print 'total_seq ', total_seq
    next_section_str = 'files'
    section = config.sections()
    if total_seq > last_total_req:
        sections = config.sections()
        for section in sections:
            if section == next_section_str:
                for conf in config.items(section):
                    name = conf[0]
                    seq = conf[1]
                    print name, seq
                    if name not in files:
                        sftp.get(remote_pre+name, local_pre+name)
if __name__ == '__main__':
    #multi_process_test()
    test_get()
