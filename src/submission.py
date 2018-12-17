import saga
import logging
import data as Data

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
        for machine_id in self.config.get_machine_list():
            self.connect(machine_id)
            for job_id in self.config.get_job_list():
                self.upload(job_id)
                self.submit(job_id)
                self.download(job_id)

    def connect(self, machine):
        """Stablish SSH connection with remote cluster"""

        try:
            ctx = saga.Context(self.config.get_server(machine).get_protocol())
            ctx.user_id = self.config.get_server(machine).get_user()
            session = saga.Session()
            session.add_context(ctx)
        except saga.SagaException, ex:
            logging.error("Job: ", str(ex))

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


    def upload(self, job_id):
        """Upload all files listed in jobs.conf
        """
        upload_files = self.config.get_jobs(job_id).get_upload_files()
        upload_to = self.config.get_jobs(job_id).get_upload_to()
        logging.info("SUMI: uploading files")
        if (not upload_files or not upload_to):
            logging.info("SUMI: no data to be uploaded")
            return
        d = Data.Data(self.config)
        d.upload(upload_files, upload_to)
        return


    def download(self, job_id):
        """Download all file listed in jobs.conf
        """
        download_files = self.config.get_jobs(job_id).get_download_files()
        download_to = self.config.get_jobs(job_id).get_download_to()
        logging.info("SUMI: downloading files")
        if (not download_files or not download_to):
            logging.info("SUMI: no data to be downloaded")
            return
        d = Data.Data(self.config)
        d.download(download_files, download_to)
        return
