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

## Build and Tests

Under construction

## TODO

- [ ] ( Normal ) Validate data insertion on database;
- [ ] (  Hard  ) Create endpoint for data import;
- [ ] (  Hard  ) Create routine for data processing (alternatives: Apscheduler/Celery).

## API references

FastAPI: https://fastapi.tiangolo.com/
Example: https://github.com/tiangolo/full-stack-fastapi-template
