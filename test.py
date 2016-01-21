import os
import time
from multiprocessing import Process, Pool
import paramiko
from paramiko_client import ParamikoClient
import gevent

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

if __name__ == '__main__':
    #multi_process_test()
    test_gevent()
