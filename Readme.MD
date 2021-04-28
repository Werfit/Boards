# Boards
## Installation

Firstly, clone the repository

<pre>git clone https://github.com/Werfit/Boards</pre>
Secondly, install all requirments

<pre>pip install</pre>
  
## Set up

Create `.env` file in the root directory. It's supposed to have `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` fields.
```
  SECRET_KEY=(your secret key)
  DEBUG=True
  ALLOWED_HOSTS=.localhost,127.0.0.1
```

Then create database
<pre>python manage.py makemigrations</pre>
<pre>python manage.py migrate</pre>

Finally, you can run the server
<pre>python manage.py runserver</pre>
