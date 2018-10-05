import unittest
import os.path
import paramiko

class TestData(unittest.TestCase):

    def test_connection(self):
        username="sumi"
        hostname="localhost"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username)
        sftp.close()
        ssh.close()
        
    def test_download(self):
        datafile = "test.txt"
        data = Data(conf)
        data.download(args.down)
        assert os.path.isfile(datafile) 
        
    def test_upload(self):
        datafile = "test.txt"
        data = Data(conf)
        data.upload(args.up)
