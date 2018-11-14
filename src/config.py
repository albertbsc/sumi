import ConfigParser
import os
import logging

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
        self.udocker    = None
        self.arguments  = None
        self.cpus       = None
        self.time       = None
        self.name       = None
        self.threads    = None

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
        #self.server = ServerConfig()
        #self.jobs = JobConfig()
        self.server = None
        self.jobs = None
        self.selected_jobs = []
        self.selected_servers = []

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
        for server_id in config.sections():
            if(self.server == None):
                self.server = {}    #Initialize dictionary
            self.server[server_id] = ServerConfig()
            self.server[server_id].set_manager(config.get(server_id, 'manager'))
            self.server[server_id].set_server(config.get(server_id, 'server'))
            self.server[server_id].set_user(config.get(server_id, 'user'))
            self.server[server_id].set_protocol(config.get(server_id, 'protocol'))

    def load_jobs(self):
        """Load jobs.conf file"""
        if not os.path.exists(self.file_jobs):
            raise IOError, self.file_jobs + " does not exist"

        config = ConfigParser.ConfigParser()
        config.read(self.file_jobs)

        for job_id in config.sections():
            if(self.jobs == None):
                self.jobs = {}
            self.jobs[job_id] = JobConfig()
            self.jobs[job_id].set_udocker(config.get(job_id, 'udocker'))
            self.jobs[job_id].set_arguments(config.get(job_id, 'arguments'))
            self.jobs[job_id].set_cpus(config.get(job_id, 'cpus'))
            self.jobs[job_id].set_time(config.get(job_id, 'time'))
            self.jobs[job_id].set_threads(config.get(job_id, 'threads_per_process'))
            self.jobs[job_id].set_name(job_id)

    def get_server(self, key):
        return self.server[key]

    def get_jobs(self, key):
        return self.jobs[key]

    def get_machine_list(self):
        return self.selected_servers

    def get_job_list(self):
        return self.selected_jobs

    def set_selected_jobs(self, jobs):
        for job in jobs:
            if job not in self.jobs:
                logging.warning("Job " + job + " does not exist")
            else:
                self.selected_jobs.append(job)
        if(len(self.selected_jobs) == 0):
            logging.error("Specified jobs do not exist. Check your configuration")
            raise Exception, "No valid job identifiers"

    def set_selected_servers(self, servers):
        for server in servers:
            if server not in self.server:
                logging.warning("Server " + server + " does not exist")
            else:
                self.selected_servers.append(server)
        if(len(self.selected_servers) == 0):
            logging.error("Specified servers do not exist. Check your configuration")
            raise Exception, "No valid server identifiers"
