Scenario 1: Reset migrations by dropping the database

Remove all migrations files within your project. Go through each of your project's apps migration folders and remove everything inside, except the __init__.py file.

In Linux based system, you can open your terminal and change your directory to the root of the project where manage.py is located and run these to remove all migration files.

    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -delete

This will remove all migration files except __init__.py.

The next step is to drop the current database:

    If you are using db.sqlite3, you can remove it by running rm -rf db.sqlite3
    If you are using something like MySQL or PostgreSQL then you have to manually delete the database and then create the DB again.

Once DB is dropped and recreated, create the initial migrations and generate the database schema using

python manage.py makemigrations 
python manage.py migrate

That's all, it will apply to all the migrations. You can check out other django-tutorials
Scenario 2: Reset migrations without dropping database

This is useful and ideal for resetting migration for large apps where you have a big database. Make sure your models fit the current database schema. The easiest way to do it is by trying to create new migrations:

python manage.py makemigrations

If there are any pending migrations, apply them first. If you see the below message, You are good to go.

No changes detected

Now you will need to clear the migration history app by app. First, run the showmigrations command so we can keep track of what is going on:

python manage.py showmigrations

admin 
[X] 0001_initial 
[X] 0002_logentry_remove_auto_add 
auth 
[X] 0001_initial 
[X] 0002_alter_permission_name_max_length 
[X] 0003_alter_user_email_max_length 
[X] 0004_alter_user_username_opts 
[X] 0005_alter_user_last_login_null 
[X] 0006_require_contenttypes_0002 
[X] 0007_alter_validators_add_error_messages 
contenttypes 
[X] 0001_initial 
[X] 0002_remove_content_type_name 
core 
[X] 0001_initial 
[X] 0002_remove_mymodel_i 
[X] 0003_mymodel_bio 
sessions 
[X] 0001_initial

Clear the migration history (please note that core is the name of my app)

python manage.py migrate --fake core zero

The result will be something like this:

Operations to perform: 
Unapply all migrations: core 
Running migrations: 
Rendering model states... 
DONE 
Unapplying core.0003_mymodel_bio... FAKED 
Unapplying core.0002_remove_mymodel_i... FAKED 
Unapplying core.0001_initial... FAKED

Now run the command python manage.py showmigrations again

admin 
[X] 0001_initial 
[X] 0002_logentry_remove_auto_add 
auth 
[X] 0001_initial 
[X] 0002_alter_permission_name_max_length 
[X] 0003_alter_user_email_max_length 
[X] 0004_alter_user_username_opts 
[X] 0005_alter_user_last_login_null 
[X] 0006_require_contenttypes_0002 
[X] 0007_alter_validators_add_error_messages 
contenttypes 
[X] 0001_initial 
[X] 0002_remove_content_type_name 
core 
[ ] 0001_initial 
[ ] 0002_remove_mymodel_i 
[ ] 0003_mymodel_bio 
sessions
 [X] 0001_initial

You must do that for all the apps you want to reset the migration history.

Now, remove the actual migration files. Go through each of your project's app migration folders and remove everything inside, except for the __init__.py file.

    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -delete

It will remove all the migrations files inside your project. Run the python manage.py showmigrations again.

admin 
[X] 0001_initial 
[X] 0002_logentry_remove_auto_add 
auth 
[X] 0001_initial 
[X] 0002_alter_permission_name_max_length 
[X] 0003_alter_user_email_max_length 
[X] 0004_alter_user_username_opts 
[X] 0005_alter_user_last_login_null 
[X] 0006_require_contenttypes_0002 
[X] 0007_alter_validators_add_error_messages 
contenttypes 
[X] 0001_initial 
[X] 0002_remove_content_type_name 
core 
(no migrations) 
sessions 
[X] 0001_initial

Create the initial migrations, run python manage.py makemigrations

Migrations for 'core': 
0001_initial.py:  
-Create model MyModel

In this case, you won’t be able to apply the initial migration because the database table already exists. What we want to do is to fake this migration instead. Run command

python manage.py migrate --fake-initial

Operations to perform: 
Apply all migrations: 
admin, core, contenttypes, auth, sessions 
Running migrations: 
Rendering model states... DONE 
Applying core.0001_initial... FAKED

Run python manage.py showmigrations again

admin 
[X] 0001_initial 
[X] 0002_logentry_remove_auto_add 
auth 
[X] 0001_initial 
[X] 0002_alter_permission_name_max_length 
[X] 0003_alter_user_email_max_length 
[X] 0004_alter_user_username_opts 
[X] 0005_alter_user_last_login_null 
[X] 0006_require_contenttypes_0002 
[X] 0007_alter_validators_add_error_messages 
contenttypes 
[X] 0001_initial 
[X] 0002_remove_content_type_name 
core 
[X] 0001_initial sessions 
[X] 0001_initial

That's all. You should have fresh migration files by now. I hope this helped. Do checkout the free django newsletter. Check out more django-tutorials. If you want to structure a Django project, then you check out this article on structuring a Django app for beginners.

© 2018 - 2023 Nitin Raturi. All Rights Reserved.

    Home
    Privacy
    Cookies
    Newsletter
    Sitemap
    RSS

