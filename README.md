in# package_template
A Template to build a PIP package## Authors- [@alod83](https://www.github.com/alod83)
## InstallationInstall my-project with pip
```bash
  pip install em4-datastore-py3
```
## Requirements
* numpy
##py -m pip install --upgrade build
##py -m build

## py -m venv venv

## pip freeze > requirements.txt

## pip install -t lib -r requirements.txt

## gcloud init

## gcloud app deploy app.yaml

## gcloud app deploy cron.yaml

## gcloud beta emulators datastore start --data-dir=C:\Steve\workspaces\PycharmProjects\emdir --project test --host-port “127.0.0.1:8001”
## cd venv/scripts
## activate
## pip install git+https://git@github.com/4-0-analytics/em4-datastore-py3.git
## pip install git+https://git@github.com/4-0-analytics/em4-datastore-py3.git --upgrade
## pip install git+https://git@github.com/4-0-analytics/em4-datastore-py3.git -t lib

## pip uninstall -r uninstallpackage.txt
## pip install -t lib -r uninstallpackage.txt

## https://github.com/4-0-analytics/40-analytics-dev.git

## echo "# 40-analytics-dev" >> README.md
## git init
## git add README.md
## git commit -m "first commit"
## git branch -M main
## git remote add origin https://github.com/4-0-analytics/40-analytics-dev.git
## git push -u origin main

## …or push an existing repository from the command line

## git remote add origin https://github.com/4-0-analytics/40-analytics-dev.git
## git branch -M main
## git push -u origin main

## to popup setup screen : ctrl alt S

pip install virtualenv
virtualenv venv
pip install Django
django-admin startproject 40-analytics-backend
pip install djangorestframework
pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
The Commands¶

There are several commands which you will use to interact with migrations and Django’s handling of database schema:

    migrate, which is responsible for applying and unapplying migrations.
    makemigrations, which is responsible for creating new migrations based on the changes you have made to your models.
    sqlmigrate, which displays the SQL statements for a migration.
    showmigrations, which lists a project’s migrations and their status.

You should think of migrations as a version control system for your database schema. makemigrations is responsible for packaging up your model changes into individual migration files - analogous to commits - and migrate is responsible for applying those to your database.
######################################################
pip freeze > requirements.txt
virtualenv venv
pip install -t lib -r requirements.txt
pip install djangorestframework
django-admin startproject analytics_rest_api
python manage.py runserver
python manage.py startapp emcar
=> add 'rest_framework' into INSTALLED_APPS = [
                                               ...
                                               'rest_framework',
                                               'emcar'
                                               ]
pip install psycopg2
pip install django-cors-headers
=>INSTALLED_APPS = [
    ...
    # CORS
    'corsheaders',
]
=>MIDDLEWARE = [
    ...
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
=>Next, set CORS_ORIGIN_ALLOW_ALL and add the host to CORS_ORIGIN_WHITELIST:

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8081',
)
python manage.py makemigrations emcar
python manage.py migrate emcar
#create all kinds of auth tables
python manage.py migrate --database emcardb
=>Create a urls.py inside emcar app 
from django.urls import path, re_path
from emcar import views

urlpatterns = [
    re_path(r'^api/emcar', views.tutorial_list),
    re_path(r'^api/emcar/(?P<pk>[0-9]+)$', views.tutorial_detail),
    re_path(r'^api/emcar/published$', views.tutorial_list_published),
    path('basic', views.YourView.as_view())
]
=>Open analytics_rest_api/urls.py
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('emcar.urls'))
]
python manage.py runserver 8080
python manage.py createsuperuser (admin, admin@email.com, and adminpass123)

(.venv) $ rm db.sqlite3
(.venv) $ rm -r emcar/migrations
(.venv) $ python manage.py makemigrations emcar
(.venv) $ python manage.py migrate





python manage.py sqlmigrate emcar 0001
python manage.py migrate
 
# snippets/admin.py
from django.contrib import admin
from .models import Trip

admin.site.register(Trip)

python manage.py createsuperuser (admin, admin@email.com, and adminpass123)

python manage.py runserver

=>careate analytics_trip/serializers.py, analytics_trip/urls.py

=>modify models.py add owner and highlight fields
rm db.sqlite3
rm -r analytics_trip/migrations
python manage.py makemigrations analytics_trip
python manage.py migrate

pip install -Iv psycopg2==2.9.5

python manage.py createsuperuser (admin, admin@email.com, and adminpass123)
python manage.py createsuperuser (test, test@email.com, and testpass123)
python manage.py runserver

http://127.0.0.1:8000/admin/


#####################################################################
=>class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)

    class Meta:
        managed = False
=>delete 0001_initial.py
python manage.py makemigrations
python manage.py migrate --fake emcar zero
python manage.py migrate --fake-initial


###############################################################


python manage.py migrate --database emcardb


#########################github repository #####################

https://github.com/4-0-analytics/4-0-analytics-postgresql.git

CREATE SCHEMA IF NOT EXISTS emcarsref
    AUTHORIZATION devuser;

GRANT ALL ON SCHEMA emcarsref TO devuser;
################################################
Steve's phone ip address: 49.216.98.100
Steve's Home ip address:  68.198.219.232


######################### deploy django to aws eb #####################
pip install awsebcli --upgrade
eb init -p python-3.11 40-analytics-auto
eb init
eb init -i
eb create
eb platform select
#eb create django-env
#MyElasticBeanstalkApp
eb create --vpc.id vpc-0d1cb06b --elb-type application 
eb create --vpc.id vpc-0d1cb06b --vpc.elbsubnets subnet-edeefea4,subnet-0d06f86b i-0080a403d9b821264
#eb create --vpc.id vpc-095d18d6bd7ee6033 --elb-type classic
aws ec2 describe-instance-status --include-all-instances
i-0f3447d2205c45416,i-00e1c7539c72b0df3


eb create --vpc.id vpc-095d18d6bd7ee6033  --vpc.dbsubnets subnet-0ab5e2c402d101365,subnet-id2 --vpc.ec2subnets subnet-id1,subnet-id2
eb create --vpc.id vpc-09394eaf3b3a0f5e7  --vpc.dbsubnets subnet-0ebcf1fdd1e1c22bc,subnet-id2 --vpc.ec2subnets subnet-id1,subnet-id2
eb create django-env --elb-type classic
eb status
eb deploy
eb open


eb create \
    --elb-type application \
    --region us-east-1 \
    --platform "64bit Amazon Linux 2015.09 v2.0.6 running Docker 1.7.1" \
    --version my-version \
    --vpc.id <vpc to launch into> \
    my-environment-name

 aws ec2 describe-vpcs --region us-east-2
 
40analyticsauto.us-east-2.elasticbeanstalk.com