import ConfigParser
import os

class ServerConfig(object):
    """Data structure to store server configuration"""

    def __init__(self):
        self.manager = None
        self.server = None
        self.user = None
        self.protocol = "ssh"
        
    def set_manager(self, manager):
        self.manager = manager
            
    def set_server(self, server):
        self.server = server

    def set_user(self, user):
        self.user = user
        
    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_manager(self):
        return self.manager
        
    def get_server(self):
        return self.server

    def get_user(self):
        return self.user

    def get_protocol(self):
        return self.protocol

class JobConfig(object):
    """Data structure to store jobs configuration"""
    def __init__(self):
        self.udocker = None
        self.arguments = None
        self.cpus = None
        self.time = None
        self.name = None
        self.threads = None

    def set_udocker(self, udocker):
        self.udocker = udocker

    def set_arguments(self, arguments):
        self.arguments = arguments

    def set_cpus(self, cpus):
        self.cpus = cpus

    def set_time(self, time):
        self.time = time

    def set_threads(self, threads):
        self.threads = threads

    def set_name(self, name):
        self.name = name
        
    def get_udocker(self):
        return self.udocker
        
    def get_arguments(self):
        return self.arguments
        
    def get_cpus(self):
        return self.cpus
        
    def get_time(self):
        return self.time
        
    def get_threads(self):
        return self.threads
        
    def get_name(self):
        return self.name


class Config(object):
    """
    Load and store server and jobs configuration
    """

    __instance = None
    
    def __init__(self):
        self.conf = None
        self.home = os.path.expanduser("~") # Get home directory
        self.home = self.home + "/.sumi/"
        self.file_server = self.home + "servers.conf"
        self.file_jobs = self.home + "jobs.conf"
        self.server = ServerConfig()
        self.jobs = JobConfig()
        
    
    def __new__(cls, *args, **kwargs):
        """Singleton"""
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
    

    def load_server(self):
        """Load servers.conf file"""
        if not os.path.exists(self.file_server):
            raise IOError, self.file_server + " does not exist"
    
        config = ConfigParser.ConfigParser()
        config.read(self.file_server)
        #print self.file_server
        for cluster in config.sections():
            self.server.set_manager(config.get(cluster, 'manager'))
            self.server.set_server(config.get(cluster, 'server'))
            self.server.set_user(config.get(cluster, 'user'))
            self.server.set_protocol(config.get(cluster, 'protocol'))

    def load_jobs(self):
        """Load jobs.conf file"""
        if not os.path.exists(self.file_jobs):
            raise IOError, self.file_jobs + " does not exist"

        config = ConfigParser.ConfigParser()
        config.read(self.file_jobs)

        for jobs in config.sections():
            self.jobs.set_udocker(config.get(jobs, 'udocker'))
            self.jobs.set_arguments(config.get(jobs, 'arguments'))
            self.jobs.set_cpus(config.get(jobs, 'cpus'))
            self.jobs.set_time(config.get(jobs, 'time'))
            self.jobs.set_threads(config.get(jobs, 'threads_per_process'))
            self.jobs.set_name(jobs)
            

    def get_server(self):
        return self.server

    def get_jobs(self):
        return self.jobs

