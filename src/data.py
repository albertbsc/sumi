from __future__ import print_function
import paramiko
import glob
import os
import logging
import datetime

class Data(object):

    def __init__(self, config):
        """
        This module implements the methods to transfer data between the local
        machine and remote clusters.

        Attributes:
            server (obj): Contains information of the server configuration.
        """

        self.config = config
        #self.server = config.get_server()

    def upload(self, origin, destination):
        """Upload a local file to the remote server.

        Args:
            fd (str): Path to local file.
        """
        for machine in self.config.get_machine_list():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.config.get_server(machine).get_server(), \
                username=self.config.get_server(machine).get_user())
            sftp = ssh.open_sftp()

            # Use glob to handle wildcards
            file_list = glob.glob(origin)
            for file in file_list:
                path, file_name = os.path.split(file)
                logging.info("SUMI: scp " + file + "   " + destination)
                sftp.put(file, destination + "/" + file_name, callback=transfer_progress)
            sftp.close()
            ssh.close()

    def download(self, origin, destination):
        """Download a remote file to local.

        Args:
            fd (str): Path to remote file.
        """
        for machine in self.config.get_machine_list():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.config.get_server(machine).get_server(), \
                username=self.config.get_server(machine).get_user())
            # Get files according to wildcards
            stdin, stdout, stderr = ssh.exec_command('ls ' + origin)
            file_list = stdout.read().split()
            sftp = ssh.open_sftp()
            for file in file_list:
                path, file_name = os.path.split(file)
                logging.info("SUMI: scp " + file + "   " + destination)
                sftp.get(file, destination + "/" + file_name, callback=transfer_progress)
            sftp.close()
            ssh.close()

def transfer_progress(transferred, total):
    now = datetime.datetime.now()
    print("{0}/{1}/{2} {3}:{4}:{5} INFO     progress {6:.2f}%\r".format(now.year,\
         now.month, now.day, now.hour, now.minute, now.second,\
         100*float(transferred)/float(total), ), end='\r')
