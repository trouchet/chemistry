# ApI
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%20|%203.8%20|%203.9-blue)](https://www.python.org/downloads/)
[![FastAPI Version](https://img.shields.io/badge/FastAPI-0.68.1-blue)](https://fastapi.tiangolo.com/)
[![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-13-blue)](https://www.postgresql.org/)


This is a minimal repository for a FastAPI app instance with: 
    - Database: _postgres_;
    - ORM: _SQLAlchemy_;
    - Monitoring: _prometheus_.

## Get started

For installation of packages on file `requirements.txt`, run the command on terminal according to your operational system. 

1. Window/Linux/MacOSs: 
    a. Navigate to root folder; 
    b. Install with command run `pip install -r requirements.txt`.

2. API references
    Tools: FastAPI: https://fastapi.tiangolo.com/
    	
## Deployment

1. Change the environment variables on `.env` file;
    a. Change variable ENVIRONMENT to `production`;
    b. Change the non-test database credentials to your remote database configuration;
    c. Change the variable `SECRET_KEY` to some trustworthy string;

2. Run command `docker compose up`;

## Build and Tests

Under construction

## TODO

- [ ] ( Normal ) Validate data insertion on database;
- [ ] (  Hard  ) Create endpoint for data import;
- [ ] (  Hard  ) Create routine for data processing (alternatives: Apscheduler/Celery).
