import saga
import logging

class Submission(object):
    """
    This module implements the methods to submit the jobs using the SAGA
    library.

    Attributes:
        config (obj): Contains job and server configuration.
        js     (obj): Contains SAGA connection.
    """

    def __init__(self, config):
        self.config = config
        self.js = None

    def run(self):
        for machine in self.config.get_machine_list(): # TODO
            self.connect(machine)
            for job in self.config.get_job_list(): # TODO
                self.submit(job)

    def connect(self, machine):
        """Stablish SSH connection with remote cluster"""

        ctx = saga.Context(self.config.get_server(machine).get_protocol())
        ctx.user_id = self.config.get_server(machine).get_user()
        session = saga.Session()
        session.add_context(ctx)

        try:
            url = self.config.get_server(machine).get_manager() + "+" + \
                self.config.get_server(machine).get_protocol() + "://" + \
                self.config.get_server(machine).get_server()
            self.js = saga.job.Service(url, session=session)
        except saga.exceptions.AuthenticationFailed:
            logging.error("Job: Authentication failed")
            raise saga.exceptions.AuthenticationFailed

    def submit(self, job):
        """Submit job with the configured job and machine
        
        Returns:
            int: The job exit code. 0 if successful.
        """

        #Job description
        jd = saga.job.Description()

        # Set job configuration
        jd.executable      = self.config.get_jobs(job).get_udocker()
        jd.arguments       = self.config.get_jobs(job).get_arguments()
        jd.threads_per_process = self.config.get_jobs(job).get_threads()
        jd.total_cpu_count = self.config.get_jobs(job).get_cpus()
        jd.wall_time_limit = self.config.get_jobs(job).get_time()
        jd.output          = self.config.get_jobs(job).get_name() + "-%J.stdout"
        jd.error           = self.config.get_jobs(job).get_name() + "-%J.stderr"
        
        #Create job and run
        job = self.js.create_job(jd)
        job.run()

        logging.info("Job: starting ")
        logging.info("Job: ID %s" % (job.id))
        logging.info("Job: state %s" % (job.state))
        logging.info("Job: waiting")

        #Monitor
        job.wait()

        logging.info("Job: State %s" % (job.state))
        logging.info("Job: Exitcode %s" % (job.exit_code))

        if job.exit_code != "0":
            logging.error("Job: failed, check your job configuration")
        
        return int(job.exit_code)


