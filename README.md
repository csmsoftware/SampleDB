# Welcome to SampleDB

![alt text](https://github.com/csmsoftware/SampleDB/blob/master/sampledbapp/static/img/sampledb-logo-220.png "SampleDB")

SampleDB is an open-source Python/Django web application for recording the physical location of pseudo-anonymised samples, in line with the Human Tissue Act (HTA) and the General Data Protection Regulation (GDPR).

Developed by [Gordon Haggart](https://github.com/ghaggart) for Imperial College London.

Apache 2 licence. 

## Data model

1. Each project lead/PI is a GDPR/HTA data owner, and has a *Group* with allowed users.
2. Each *Group* contains *Projects*, and each *Project* contains *Samples*.
3. Each *Sample* contains the fields necessary for recording the sample type, storage location, consent form information and tissue bank reference.

![Data model](https://github.com/csmsoftware/SampleDB/blob/master/readme-img/sampledb_datamodel.png "SampleDB")

The fields recorded by the system are fixed/hard-coded, and are: 

* Study title - *Project* collections can be subdivided into *Studies*.
* Sample ID - The sample identifier - must be unique by study_title.
* Species - Human or *?*
* Sample Matrix - Sample type - ie 'Serum'.
* Collection Protocol - How the sample has been processed - ie 'Filtered'.
* Campus - Which campus is the sample stored in?
* Building - Which building is the sample stored in?
* Room - Which room is the sample stored in?
* Freezer ID - Which freezer is the sample stored in?
* Shelf ID - Which freezer shelf is the sample stored in?
* Box ID - Which box is the sample stored in?
* Consent Form Information - Record where the consent forms are stored, or the REC number.
* Tissue Bank Reference - The Tissue Bank Collection ID.
* Parent ID - May be used for pseudo-anonymised subject identifiers.
* Parent Type - What kind of pseudo-anonymised identifier?

## Usage/Features

* Create *Groups*.
* Assign *Users* to *Groups*.
* Create *Projects*.
* Upload *Samples* from XLS file.
* Export *Samples* to XLS file.
* Edit *Samples*.
* Delete *Samples*.
* Move *Samples* to another *Project*.
* Auditing.
* Presubmission data validation.
* Offline/asynchronous processing.
* Historical records for auditing/security. (Requires [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/) package).

## Requirements

* Python3.6
* SQLite3/PostgreSQL/MySQL
* Nginx/Apache
* uWSGI/Gunicorn
* Redis

* pip requirements.txt

## Installation - Centos 7/RHEL

1. Clone/download this repository

```
git clone https://github.com/csmsoftware/SampleDB.git
```

2. Install Python3.6, create new Virtualenv and activate it

```
virtualenv -p /path/to/python3.6/bin /path/to/virtualenv
source /path/to/virtualenv/bin/activate
```

3. Install and configure DB backend (SQLite3/PostgreSQL/MySQL)
 
4. Install Redis and run Redis

```
sudo yum install redis
sudo systemctl start redis.service
sudo systemctl enable redis.service
```

5. Install the pip requirements
```
pip3.6 install -r requirements.txt
```

6. Install Redis and run Redis
```
sudo yum install redis
sudo systemctl start redis.service
sudo systemctl enable redis.service
```

7. Install Nginx and configure
```
sudo yum install nginx
sudo systemctl start nginx.service
sudo systemctl enable nginx.service
```

8. Configure Gunicorn for WSGI

9. Edit the settings.py file for your own configuration - see the [Django docs](https://docs.djangoproject.com/en/2.0/) for more information

10. Migrate the database
```
/path/to/virtualenv/bin/python3.6 SampleDB/manage.py makemigrations
/path/to/virtualenv/bin/python3.6 SampleDB/manage.py migrate
```

12. Create a superuser - for logging into /admin
```
/path/to/virtualenv/bin/python3.6 SampleDB/manage.py createsuperuser
```

13. Collect the static content
```
/path/to/virtualenv/bin/python3.6 SampleDB/manage.py collectstatic
```

14. Configure crontab for the queue failure processing
```
crontab -e

# Process the RQ worker failure queue - every 5 mins.
*/5 * * * * /path/to/virtualenv/bin/python3.6 /path/to/sampledb/manage.py processjobfailures

# Clear the RQ worker failure queue - every night at 3.02am
2 3 * * * /path/to/virtualenv/bin/python3.6 /path/to/sampledb/manage.py clearfailurequeue
```

15. Configure service to run the rqworker queue (runs the offline job queue) 
```
/path/to/virtualenv/bin/python3.6 manage.py rqworker default
```

That's it. Please report any issues using the Github Issue Tracker. 

Logo adapted from here:
https://www.freevector.com/chemistry-vector
FreeVector.com

© - Imperial College London, 2018 - All rights reserved.

