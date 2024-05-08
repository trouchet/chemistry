# ApI
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%20|%203.8%20|%203.9-blue)](https://www.python.org/downloads/)
[![FastAPI Version](https://img.shields.io/badge/FastAPI-0.110.1-blue)](https://fastapi.tiangolo.com/)
[![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-13-blue)](https://www.postgresql.org/)

This is a minimal repository for a FastAPI app instance with: 

- **Database**: _postgres_;
- **ORM**: _SQLAlchemy_;
- **Monitoring**: _prometheus_.

## Get started

For installation of packages on file `requirements.txt`, run the command on terminal according to your operational system. 

* Window/Linux/MacOSs: 
    - Navigate to root folder; 
    - Install with command run `pip install -r requirements.txt`.
    	
## Deployment

* Change the environment variables on `.env` file;
    - Change variable ENVIRONMENT to `production`;
    - Change the non-test database credentials to your remote database configuration;
    - Change the variable `SECRET_KEY` to some trustworthy string;

* Run command `docker compose up`;

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

## How To Use It - Alternative With Copier

This repository also supports generating a new project using [Copier](https://copier.readthedocs.io).

It will copy all the files, ask you configuration questions, and update the `.env` files with your answers.

<details>
### Install Copier

You can install Copier with:

```bash
pip install copier
```

Or better, if you have [`pipx`](https://pipx.pypa.io/), you can run it with:

```bash
pipx install copier
```

**Note**: If you have `pipx`, installing copier is optional, you could run it directly.

### Generate a Project With Copier

Decide a name for your new project's directory, you will use it below. For example, `my-awesome-project`.

Go to the directory that will be the parent of your project, and run the command with your project's name:

```bash
copier copy https://github.com/tiangolo/full-stack-fastapi-template my-awesome-project --trust
```

If you have `pipx` and you didn't install `copier`, you can run it directly:

```bash
pipx run copier copy https://github.com/tiangolo/full-stack-fastapi-template my-awesome-project --trust
```

**Note** the `--trust` option is necessary to be able to execute a [post-creation script](https://github.com/tiangolo/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py) that updates your `.env` files.

### Input Variables

Copier will ask you for some data, you might want to have at hand before generating the project.

But don't worry, you can just update any of that in the `.env` files afterwards.

The input variables, with their default values (some auto generated) are:

- `project_name`: (default: `"FastAPI Project"`) The name of the project, shown to API users (in .env).
- `stack_name`: (default: `"fastapi-project"`) The name of the stack used for Docker Compose labels and project name (no spaces, no periods) (in .env).
- `secret_key`: (default: `"changethis"`) The secret key for the project, used for security, stored in .env, you can generate one with the method above.
- `first_superuser`: (default: `"admin@example.com"`) The email of the first superuser (in .env).
- `first_superuser_password`: (default: `"changethis"`) The password of the first superuser (in .env).
- `smtp_host`: (default: "") The SMTP server host to send emails, you can set it later in .env.
- `smtp_user`: (default: "") The SMTP server user to send emails, you can set it later in .env.
- `smtp_password`: (default: "") The SMTP server password to send emails, you can set it later in .env.
- `emails_from_email`: (default: `"info@example.com"`) The email account to send emails from, you can set it later in .env.
- `postgres_password`: (default: `"changethis"`) The password for the PostgreSQL database, stored in .env, you can generate one with the method above.
- `sentry_dsn`: (default: "") The DSN for Sentry, if you are using it, you can set it later in .env.
</details>

## Documentation

### Backend Development

Backend docs: [backend/README.md](./backend/README.md).

### Deployment

Deployment docs: [deployment.md](./deployment.md).

### Development

General development docs: [development.md](./development.md).

This includes using Docker Compose, custom local domains, `.env` configurations, etc.

- [ ] ( Normal ) Validate data insertion on database;
- [ ] (  Hard  ) Create endpoint for data import;
- [ ] (  Hard  ) Create routine for data processing (alternatives: Apscheduler/Celery).

## API references

FastAPI: https://fastapi.tiangolo.com/
Example: https://github.com/tiangolo/full-stack-fastapi-template
