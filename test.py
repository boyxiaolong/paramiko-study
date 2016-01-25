import os
import time
from multiprocessing import Process, Pool
import paramiko
from paramiko_client import ParamikoClient
import gevent
import ConfigParser
import threading

task_num = 10
begin = time.time()
is_gevent = False

lock = threading.Lock()

def func():
    global task_num
    client = ParamikoClient('config.ini')
    print client.connect()
    client.run_command('date')
    lock.acquire()
    task_num -= 1
    if task_num == 0:
        print 'elaspe ', time.time()-begin
    lock.release()

def gevent_func():
    global task_num
    client = ParamikoClient('config.ini')
    gevent.sleep(0)
    print client.connect()
    gevent.sleep(0)
    client.run_command('date')
    task_num -= 1
    if task_num == 0:
        print 'elaspe ', time.time()-begin

def multi_thread_test():
    global  task_num
    for i in range(task_num):
        threading.Thread(target=func).start()

def multi_process_test():
    pool = Pool()
    results = []
    for i in range(3):
        results.append(pool.apply_async(func))
    pool.close()
    pool.join()

def test_gevent():
    global task_num
    task_list = []
    for i in range(task_num):
        task_list.append(gevent.spawn(gevent_func))
    gevent.joinall(task_list)

def test_seq_task():
    global task_num
    for i in range(task_num):
        func()
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
    #test_gevent()
    #test_get()
    test_seq_task()
    #multi_thread_test()