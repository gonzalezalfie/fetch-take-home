# fetch-take-home
This is the guide to run the app of the take home. In order to do this, I'm making the following assumptions:

1. The user has a computer that can open Linux terminals, specifically terminals with the Ubuntu distribution. Even if the user has Windows as an operating system, it's possible to use the Ubuntu virtual subsystem.
2. The user has already installed `awslocal` and has the docker images of `data-takehome-localstack` and `fetchdocker/data-takehome-postgres` running.

**Note:** Why Linux? Because for a programmer, a world without Linux is a sad world.

# Install Git

If the user is reading this text file in the repository website, he has to have git installed to use the application.

Run these commands to install git:

`sudo apt-get update`

`sudo apt-get install git`

Press "yes" or "y" if needed.

# Clone the repository

Preferably, but not necessarily, go to your `home` directory. Run this command:

`cd`

Run this command to download all the necessary files:

`git clone repository`

It should create a directory called `fetch-take-home`.

We will move later to that directory, but for now stay in the `home` directory.

# Install Anaconda

Since the solution I propose uses python, let's install Anaconda.

Run the following command:

`wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh -O anaconda3.sh`

Execute the `anaconda3.sh` script:

`./anaconda3.sh`

If it fails due to permissions, run 

`chmod +x anaconda3.sh`

and try the previous step again.

Accept the default configuration. If it asks you to press Enter, do it. If it asks you to type "yes", do it as well.

Run the following command:

`source ~/.bashrc`

Finally, run this command to verify that Anaconda was successfully installed:

`conda list`

You should see something like this:

```
# packages in environment at /path/to/home:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
adal                      1.2.7                    pypi_0    pypi
aiohttp                   3.8.5                    pypi_0    pypi
aiosignal                 1.3.1                    pypi_0    pypi
annotated-types           0.5.0                    pypi_0    pypi
anyio                     4.0.0                    pypi_0    pypi
asttokens                 2.4.0                    pypi_0    pypi
async-timeout             4.0.3                    pypi_0    pypi
```

# Create a python3 environment

Run this command to create an environment that has python version 3.10.9.

`conda create -y --name python3 python=3.10.9`

We will install the python modules that the app needs to run. Before doing that, we have to install these dependencies:

`sudo apt-get install libxml2-dev libxslt-dev python-dev`

# Activate the python3 environment

To activate the environment, run this command:

`conda activate python3`

The prompt has to change. By default, it should look like this:

`(base) your_user_name@your_machine_name:~$`

When you activate the environment, the prompt has to look like this:

`(python3) your_user_name@your_machine_name:~$`

# Install the necesary python modules

To install the necessary python modules, run the following command:

`pip install boto3 pandas msticpy psycopg2 sqlalchemy`

It may take a while, but that's ok.

# Run the app

Go to the repository directory:

`cd fetch-take-home`

Add executable permissions to the `pipeline.sh` file:

`chmod +x pipeline.sh`

If it complains saying that you don't have permissions to do that, try 

`sudo chmod +x pipeline.sh`

Run the app:

`./pipeline.sh $(pwd)`

It may show some warnings related to the python code, but it shouldn't show any error messages.

The `pipeline.sh` script runs the following python scripts:

1. `read_sqs_messages.py`
2. `mask_data.py`
3. `upload_to_postgres.py`

As the names indicate, the first script reads the messages from AWS SQS and stores the relevant variables into a csv file, the second script masks the `ip` and `device_id` variables and the third script uploads the data to the `user_logins` table in the PostgreSQL server.

If you want to know in more detail about what each script does, you can read the comments in the files.

# Deactivate the environment

Finally, to deactivate the python3 environment, run this command:

`conda deactivate`

# Verify that the app works

Go to the postgres docker prompt and run this command:

`select * from user_logins;`

Originally, the `user_logins` table had 0 rows. Now you should see the uploaded data.

And that's it!

# Answers to the take home questions

**How would you deploy this application in production?**

In production, the source would be a real AWS SQS connection, so it would be needed to adapt boto3 to that. Also, it would be needed to connect to an actual Postgres server, probably mounted in RDS.

**What other components would you want to add to make this production ready?**

I think that other scripts concerning the metadata would be necessary. For example, how many rows were added in each execution.

**How can this application scale with a growing dataset?**

The application could append the new data to the table of the database dinamically. It would be necessary to convert this script into an airflow pipeline that is executed periodically.

**How can PII be recovered later on?**

To be honest, I'm not very familiarized with this type of problem, but I would think of creating a dictionary table with the original variables and the hashes. To identify the duplicates, it would be possible to join the table with itself. If that doesn't work, it would be possible to use Levenshtein distance.

**What are the assumptions you made?**

I assumed that it was possible to use a Linux distribution that uses the deb package system and that the potential user would already have the docker images running.
