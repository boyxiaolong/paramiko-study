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

def django_fun():
    client = ParamikoClient('config.ini')
    client.connect()
    remote_dir_name = '/home/sky/hailong/django_operate/'
    remote_file_name = remote_dir_name + 'django_blog.tar.gz'
    #client.upload_file('/Users/allen/alog/django_blog.tar.gz', remote_file_name)
    #client.run_command('tar -xzvf '+remote_file_name+' -C '+ remote_dir_name)
    client.run_command('source ' + remote_dir_name + 'env/bin/active')
    django_dir = remote_dir_name + 'django_blog/'
    python_dir = remote_dir_name + 'env/bin/python'
    #client.run_command('pip install -r ' + remote_dir_name + 'django_blog/' + 'requirements.txt')
    client.run_command(python_dir + django_dir + 'manage.py ' + 'check')
    client.run_command('curl ')

def func(call_arg_str):
    global task_num
    client = ParamikoClient('config.ini')
    print client.connect()
    client.run_command('date')
    cmd_list = {'su', 'root'}
    client.run_multi_seq_command(cmd_list)
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
    django_fun()