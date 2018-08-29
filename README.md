#SUMI

SUMI (SUbmission Manager for IMAS) is a developed for ITER IMAS (Integrated Modelling & Analysis Suite).

SUMI aims to launch jobs remotely to HPC machines with a uDocker installation and manage data transfer among local machine and remote file system.

---

#Dependencies

SUMI depends on two libraries: 

* [SAGA Python](https://github.com/radical-cybertools/saga-python)
* [Paramiko](http://www.paramiko.org/). Both libraries are free software.

##Installing Paramiko

To install Paramiko follow the official [installation guide](http://www.paramiko.org/installing.html).

##Installing Python Saga

To install SAGA Python follow the official [installation guide](http://saga-python.readthedocs.io/en/latest/usage/install.html).

---

#Installing SUMI

Download the source code from BitBucket

   git clone https://albertbsc@bitbucket.org/albertbsc/sumi.git 

Export the variable ```SUMI_DIR``` with the path to SUMI and include the bin directory inside the PATH variable

    export SUMI_DIR=/path/to/sumi
    export PATH=$PATH:$SUMI_DIR/bin
    chmod +x $SUMI_DIR/bin/sumi

If you want these variables to persist includes the previous lines in your ```.bashrc``` file.

---

#Passwordless connection

SAGA and Paramiko require a passwordless connection to work.

Copy your public key to the remote host

    ssh-copy-id -i ~/.ssh/id_rsa.pub username@example.com


---

#Quick start

Create a ```.sumi``` directory in your ```$HOME```

    mkdir $HOME/.sumi

Copy the sample configuration files for the jobs and the login node to the SUMI directory

    cp $SUMI_DIR/conf/*.conf $HOME/.sumi
    
Edit the file setting up the configuration of your machine and your jobs. To see all the options of sumi run ```-h```

    sumi -h

Once done your are ready to run SUMI. The option ```-r``` or ```--run``` will run the configured job.

    sumi -r

To retrieve the results use the option ```-d``` or ```--download```

    sumi -d filename.stout
