A Flask application with user management with multiple roles and groups.

## Current Issue
None at the moment. Testing will continue

### What's included?

* Blueprints
* User and permissions management
* Flask-SQLAlchemy for databases
* Flask-WTF for forms
* Flask-Assets for asset management and SCSS compilation
* Flask-Mail for sending emails
* gzip compression
* ZXCVBN password strength checker
* CKEditor for editing pages


## Setting up

##### Clone the repository

```
$ git clone 
$ cd REPO_NAME
```

##### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

##### Add Environment Variables

Create a file called `config.env` that contains environment variables. Example: ENVIRONMENT_VARIABLE=value or ENVIRONMENT_VARIABLE="value"

1. Generate secret key then there must be a `SECRET_KEY` variable declared. Follow the command below to generate:

   ```
   $ python3 -c "import secrets; print(secrets.token_hex(16))"
   ```

   Copy the 32-character string and add it to your `config.env`:

   ```
   SECRET_KEY=Generated_Random_String
   ```

2. The mailing environment variables can be set as the following.Currently set to use gmail

   ```
   MAIL_USERNAME=Gmailusername
   MAIL_PASSWORD=GmailPassword
   ```

Other useful variables include:

| Variable        | Default   | Discussion  |
| --------------- |-------------| -----|
| `ADMIN_EMAIL`   | `flask-base-admin@example.com` | email for your first admin account |
| `ADMIN_PASSWORD`| `password`                     | password for your first admin account |
| `DATABASE_URL`  | `data-dev.sqlite`              | Database URL. Can be Postgres, sqlite, etc. |
| `FLASK_CONFIG`  | `default`                      | can be `development`, `production`. |


##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Other dependencies for running locally

You will also need to install **PostgresQL**
Once installed and configures, add DEV_DATABASE_URL="postgresql://username:password@localhost/database_name" in the config.env

```
$ sudo apt-get install libpq-dev
```
```
$ sudo apt install nginx
```

##### Create the database -- currently this will create default user

```
$ python manage.py recreate_db
```

##### Create roles and group - currently this will create 2 roles ('User' & 'Administrator') and 1 group ('default')

```
$ python manage.py setup_dev
```

Note that this will create an admin user (first_name = 'Admin', last_name='Account') with email and password specified by the
`ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables.


##### To run locally, please configure the nginx. Sample nginx config is included
```
$ sudo apt install nginx
$ sudo ufw enable
$ systemctl status nginx //to check if nginx is active
$ sudo nano /etc/nginx/sites-available/<any name suitable to project> //check nginx_example
$ sudo ln -s /etc/nginx/sites-available/<any name suitable to project> /etc/nginx/sites-enabled
$ service nginx restart
```

## Running the app - the honcho command below will run the gunicorn at the same time

```
$ source env/bin/activate
$ honcho start -e config.env -f Local
```
