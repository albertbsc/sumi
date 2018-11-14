#!/usr/bin/env python

import argparse
import logging
import saga
import paramiko
import sys
from data import Data
from submission import Submission
from config import Config

if __name__ == "__main__":

    #Parse arguments
    parser = argparse.ArgumentParser(description='Submission Manager for IMAS')
    parser.add_argument("-r", "--run", action="store_true", dest="run",
        help="Run the configured job on a specific cluster")
    parser.add_argument("-u", "--upload", dest="up",
        help="Upload local file")
    parser.add_argument("-d", "--download", dest="down",
        help="Download remote file")
    parser.add_argument("-m", "--machine", nargs="+", dest="machine",
        help="List of machines were to submit")#,  required=True)
    parser.add_argument("-j", "--job", nargs="+", dest="jobs",
        help="List of jobs to be submitted")#, required=True)
    args = parser.parse_args()

    #Start logging and configure it with timestamp
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y/%m/%d %H:%M:%S')
    logging.info('SUMI: Starting')
    logging.info('SUMI: Reading local configuration')

    #Load and check ocal configuration files
    conf = Config()
    conf.load_server()
    conf.load_jobs()

    #Get machines
    if args.machine:
        conf.set_selected_servers(args.machine)
        #print(args.machine)

    #Get jobs
    if args.jobs:
        conf.set_selected_jobs(args.jobs)
        #print(args.jobs)

    #Run job
    if args.run == True:
        if not args.machine or not args.jobs:
            logging.error("SUMI: no machine or jobs specified")
            raise Exception
        logging.info('Job: configuring')
        sub = Submission(conf)
        sub.run()

    #Upload local files
    if args.up:
        if not args.machine:
            logging.error("SUMI: no machine selected")
            raise Exception
        data = Data(conf)
        data.upload(args.up)

    #Download remote files
    if args.down:
        data = Data(conf)
        data.download(args.down)

    #If no arguments are introduced
    if not (args.run or args.up or args.down):
        logging.info('SUMI: No option selected')

    logging.info('SUMI: Done')
