import os
import time
from multiprocessing import Process, Pool
from paramiko_client import ParamikoClient
import gevent
import ConfigParser
import threading

task_num = 10
begin = time.time()
is_gevent = False

lock = threading.Lock()

def func(call_arg_str):
    global task_num
    client = ParamikoClient('config.ini')
    print client.connect()
    client.run_command('date')
    lock.acquire()
    task_num -= 1
    if task_num == 0:
        print call_arg_str, ' consume ', time.time()-begin
    lock.release()

def process_func(call_arg_str):
    global task_num
    client = ParamikoClient('config.ini')
    print client.connect()
    client.run_command('date')


def multi_thread_test():
    global  task_num
    for i in range(task_num):
        threading.Thread(target=func, args=('multi_process_test', )).start()


def test_seq_task():
    global task_num
    for i in range(task_num):
        func('test_seq_task')

def multi_process_test():
    pool = Pool()
    results = []
    for i in range(task_num):
        results.append(pool.apply_async(process_func, args=('multi_process_test', )))
    pool.close()
    pool.join()
    print 'consume ', time.time()-begin


if __name__ == '__main__':
    multi_process_test()