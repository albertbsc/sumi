import paramiko

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

    def upload(self, fd):
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
            sftp.put(fd, fd)
            sftp.close()
            ssh.close()

    def download(self, fd):
        """Download a remote file to local.
        
        Args:
            fd (str): Path to remote file.
        """
        for machine in self.config.get_machine_list():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.config.get_server(machine).get_server(), \
                username=self.config.get_server(machine).get_user())
            sftp = ssh.open_sftp()
            sftp.get(fd, fd)
            sftp.close()
            ssh.close()

