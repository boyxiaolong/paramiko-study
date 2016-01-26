#!utf-8
from paramiko_client import ParamikoClient

"""
如果首次安装
1.安装virtualenv等环境变量
2.创建文件夹 /home/allen/django_operate
3.tar
4.upload tar.gz
5.untar
6.install requirements
7.run 'python manage check && runserver'
8.curl the url to visit the django server
"""

import os
from paramiko_client import ParamikoClient

class DjangoOperation:
    def __init__(self, paramiko_client):
        self.paramiko_client = paramiko_client

    def do_cmd(self):
        self.paramiko_client.run_command("tar zxf /home/allen/django.tar.gz")
        self.paramiko_client.run_command("pip install -r requirements.txt")
        self.paramiko_client.run_command("python manage.py check")
        self.paramiko_client.run_command("python manage.py runserver")

    def test_server(self):
        self.paramiko_client.run_command("curl 192.168.3.105:8000")
