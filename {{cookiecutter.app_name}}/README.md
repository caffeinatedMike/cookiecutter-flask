# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description}}

### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd {{cookiecutter.app_name}}
pip install -r requirements/dev.txt
```

You will see a pretty welcome screen.

#### Database Initialization (locally)

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration

```bash
flask db init
flask db migrate
flask db upgrade
```

## Deployment

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export DATABASE_URL="<YOUR DATABASE URL>"
flask run       # start the flask server
```

## Shell

To open the interactive shell, run

```bash
flask shell
```

By default, you will have access to the flask `app`.

## Running Tests/Linter

To run all tests, run

```bash
flask test
```

To run the linter, run

```bash
flask lint
```

The `lint` command will attempt to fix any linting/style errors in the code. If you only want to know if the code will pass CI and do not wish for the linter to make changes, add the `--check` argument.

## Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
flask db migrate
```

This will generate a new migration script. Then run

```bash
flask db upgrade
```

To apply the migration.

For a full migration command reference, run `flask db --help`.

If you're going to deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.

{%- if cookiecutter.use_heroku == "True" %}

## Heroku

Before deploying to Heroku you should be familiar with the basic concepts of [Git](https://git-scm.com/) and [Heroku](https://heroku.com/).

Remember to add migrations to your repository. Please check `Migrations`_ section.

Since the filesystem on Heroku is ephemeral, non-version controlled files (like a SQLite database) will be lost at least once every 24 hours. Therefore, a persistent, standalone database like PostgreSQL is recommended. This application will work with any database backend that is compatible with SQLAlchemy, but we provide specific instructions for Postgres, (including the required library `psycopg2-binary`).

**Note:** `psycopg2-binary` package is a practical choice for development and testing but in production it is advised to use the package built from sources. Read more in the [psycopg2 documentation](http://initd.org/psycopg/docs/install.html?highlight=production%20advised%20use%20package%20built%20from%20sources#binary-install-from-pypi).

If you keep your project on GitHub you can use 'Deploy to Heroku' button thanks to which the deployment can be done in web browser with minimal configuration required.
The configuration used by the button is stored in `app.json` file.

<a href="https://heroku.com/deploy" style="display: block"><img src="https://www.herokucdn.com/deploy/button.svg" title="Deploy" alt="Deploy"></a>
    <br>

Deployment by using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):

* Create Heroku App. You can leave your app name, change it, or leave it blank (random name will be generated)

    ```bash
    heroku create {{cookiecutter.app_name}}
    ```

* Add buildpacks

    ```bash
    heroku buildpacks:add --index=1 heroku/python
    ```

* Add database addon which creates a persistent PostgresSQL database. These instructions assume you're using the free [hobby-dev](https://elements.heroku.com/addons/heroku-postgresql#hobby-dev) plan. This command also sets a `DATABASE_URL` environmental variable that your app will use to communicate with the DB.

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --version=11
    ```

* Set environmental variables (change `SECRET_KEY` value)

    ```bash
    heroku config:set SECRET_KEY=not-so-secret
    heroku config:set FLASK_APP=autoapp.py
    ```

* Please check `.env.example` to see which environmental variables are used in the project and also need to be set. The exception is `DATABASE_URL`, which Heroku sets automatically.

* Deploy on Heroku by pushing to the `heroku` branch

    ```bash
    git push heroku main
    ```

{%- endif %}
