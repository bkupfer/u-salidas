How to get this up and running.

1.- Download lastest version of the code

2.- Create database
      > python manage.py syncdb
   2.1- create superuser if needed

3.- Migrate changes in the database (this step may not be needed in all systems)
      > python manage.py migrate

4.- Load initial data to the database
   > python manage.py loaddata Commission_type.json
   > python manage.py loaddata test_applications.json

5.- Run the server
   > python manage.py runserver

6.- Register groups and initial users for the login system.
    To do so, enter to the following URL
      127.0.0.1:8000/admin/auth
    Here you must create groups with the following names:
      "professor"
      "magna"
      "angelica"
      "alejandro"
    All of this four groups should have at all the 'salidas' permissions given. (premissions could be more restrictive in the future)

7.- Create users (or test users) for the groups
    To do this,
      * create a new user and give it a name & password. click save
      * assign the user to one of the groups previously created

8.- Now the following URL will take you to the login page, where you can enter the site with one of the previously created users
      127.0.0.1:8000/
