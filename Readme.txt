How to get this up and running.

1.- Download lastest version
2.- python manage.py syncdb
   2.1- create superuser if needed
3.- python manage.py migrate
4.- python manage.py loaddata Commission_type.json
5.- python manage.py loaddata test_applications.json
   5.1- this could bring some errors, if it does, just ignore them.
6.- python manage.py runserver
7.- enter to the pages in 127.0.0.1:8000 (localhost:8000)

Available views.
   * for teachers
      /new_application
      /teacher_calendar
   * for administrative
      /list_of_applications
      /historic_calendar
      /application_detail

