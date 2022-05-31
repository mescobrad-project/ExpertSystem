# Expert System

![REPO-TYPE](https://img.shields.io/badge/repo--type-backend-critical?style=for-the-badge&logo=github)

The Expert System is a set of tools that allow the end-user to execute
dynamically created processes and potentially unlimited workflows.

The Expert System is executed on a closed dockerized environment (i.e., uses the
Docker container platform) and uses the Python programming language and the
FastAPI web framework. The Expert system contains various tools and libraries
based on python packages and, that can manage workflows, workflow designer tools
to create BPMN dynamic diagrams, and other components implemented via JSON
standards.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

The requirements to run, test, and develop the Expert System are:

-   [Docker](https://docs.docker.com/engine/)
-   [Docker Compose](https://docs.docker.com/compose/)
-   Linux environment is recommended
-   [Python 3.10](https://www.python.org/)
-   [Pipenv](https://pipenv.pypa.io/en/latest/) virtual environment
-   [FastAPI](https://fastapi.tiangolo.com/) Web Framework

### Installing

There are two different ways to install the application. If you want to develop
some new features, or fix some bugs, it is highly recommended to use a python
environment first and then build and test with a docker image.

But wait! Before doing anything, create an environment file based on the example
and edit the appropriate variables.

```bash
cp .env.example .env
nano .env
```

#### Python-based

First, be sure to install Python and activate version 3.10 and Pipenv:

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# If necessary, run the line bellow
sudo apt build-dep python3.10 python3-tk
```

Then check the version to be at 3.10 or greater.

```bash
python --version
```

Now it's time to install Pipenv:

```bash
pip install pipenv
```

And check if everything works as expected, by executing the following command:

```bash
pipenv --version
```

To start developing, you first instantiate the environment, install the
dependencies and start the server:

```bash
pipenv --python 3.10
pipenv install
pipenv run uvicorn src.main:main --host 0.0.0.0 --port 80 --reload
```

#### Docker-based

According to the documentation of sail, first, add the following line in the
_~/.bashrc_ file, close the terminal and open it again.

```bash
alias sail='[ -f sail ] && bash sail'
```

Run the following command to create and run the project's docker images. This
assumes that both Docker and docker-compose are installed.

```bash
sail up -d
```

## Running the tests

There are two possible ways to execute the tests. The first one is directly
through the virtual environment and the second via the sail command.

```bash
pipenv run pytest
```

or

```bash
sail up -d
sail pytest
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

To validate the coding style and be consistent, we use Black. Run the following
command to format your code:

```
pipenv run black
```

## Built With

To build the docker image of this repo, run the following command:

```bash
sail build
```

### Run Database Migrations

All database changes are monitored by a python module called "_Alembic_". All
changes in the "_./src/models_" folder will result in a revision of the database
model by typing the following:

```bash
sail alembic revision --autogenerate -m "Type message here."
```

Then sync the changes with the connected database with the command below:

```bash
sail alembic upgrade head
```

### Production build and versioning

For a production build, create a starter .env from the example and run the
previous command with cache disabled:

```bash
cp .env.example .env
sail build --no-cache
```

After the build is complete, tag the docker image with the desired version and
push it to the registry.

```bash
docker tag username/exampleimage username/exampleimage:v1.0.0
docker push username/exampleimage:v1.0.0
```

## Deployment

To deploy the application in a staging or production environment, you pull the
version you want from your docker registry and use it accordingly. Keep a note
that every time you make a version update, you have to run the migration script
to update the database up to date.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](tags).

## Authors

-   **Vassilis Stamoulos** - [doskelfsy](https://github.com/doskelfsy)

See also the list of [contributors](contributors) who participated in this
project.

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details

## Acknowledgments

-   A modded version of [Sail](https://github.com/laravel/sail)
-   Special thanks to
    [atom/atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md) and
    [opengovernment/opengovernment](https://github.com/opengovernment/opengovernment/blob/master/CONTRIBUTING.md)
    for the contributing ideas.
-   Special thanks also to [gitmoji](https://github.com/carloscuesta/gitmoji)
    for the use of emojis on GitHub commit messages.
