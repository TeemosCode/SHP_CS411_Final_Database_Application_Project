Please find the few packages needed by this project in the requirements.txt

In order for all of us to safely develop together locally, do the following:

1. Create a python virtual environment in your local development directory:

Run the following commands to get your virtual environment set up and running. Using Python3.6 because there are some issues with 3.7 and Django & MySQL so it seems (Not really sure but saw some threads about them... Still if you don't have python3.6 and think its gona be a pain to get another version, just ignore the --python=python3.6 for the second command.

=====
pip install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
=====


2. Then install the packages within the requirement.txt using the following command:

===
pip install -r requirements.txt
===


(There is a problem for me to setup mysqlclient package on my own mac, currrently I still have not found my way around it as it was pissing me off going through lots of posts and stuff and wasting my time. So instead I used mysql-connector-python. But I'm not sure if this would work if we were to really connect Django with MySQL. Need to further check this out...)


To deactivate the virtual environment. Simply type the following command:

===
deactivate
===




NOTE: Do the following FLOW:
    RUN THE DATABASE SQL SCRIPT LOCALLY TO CREATE UR DATABASE AND TABLES FIRST

    MAKE SURE django is linked to your mysql database

    THEN run "python manage.py inspectdb > models.py" -> A models.py will be created under your project. Move that to
    the backpacking application and replace the original models.py

    THEN RUN ("python manage.py migrate").
    ADD application to settings and import and register all model classes to admin.py
    (DO NOT USE "makemigrations"!!!!!)
    THEN YOU SHOULD BE ABLE TO ACCESS AND CHANGE DATA USING ADMIN IN DJANGO!
