"""Tasks for use with Invoke."""

import os
from invoke import task

PYTHON_VER = os.getenv("PYTHON_VER", "3.7")
NAUTOBOT_VER = os.getenv("NAUTOBOT_VER", "master")

GRIMLOCK_VERSION = os.getenv("GRIMLOCK_VERSION", "grimlock-integration")
GRIMLOCK_HASH = os.getenv("GRIMLOCK_HASH", "2f8bb0f")

# Name of the docker image/container
NAME = os.getenv("IMAGE_NAME", "ntc-nautobot-plugin-metrics-ext")
PWD = os.getcwd()

COMPOSE_FILE = "development/docker-compose.yml"
BUILD_NAME = "nautobot_metrics_ext"

DEFAULT_ENV = {
    "NAUTOBOT_VER": NAUTOBOT_VER,
    "PYTHON_VER": PYTHON_VER,
    "GRIMLOCK_VERSION": GRIMLOCK_VERSION,
    "GRIMLOCK_HASH": GRIMLOCK_HASH,
}

environment = DEFAULT_ENV
# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task
def build(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Build all docker images.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} build", env=DEFAULT_ENV,
    )


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Start Nautobot and its dependencies in debug mode.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    print("Starting Nautobot .. ")
    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} up", env=DEFAULT_ENV,
    )


@task
def start(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Start Nautobot and its dependencies in detached mode.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    print("Starting Nautobot in detached mode.. ")
    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} up -d", env=DEFAULT_ENV,
    )


@task
def stop(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Stop Nautobot and its dependencies.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    print("Stopping Nautobot .. ")
    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} down", env=DEFAULT_ENV,
    )


@task
def destroy(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Destroy all containers and volumes.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} down", env=DEFAULT_ENV,
    )
    context.run(
        f"docker volume rm -f {BUILD_NAME}_pgdata_nautobot_metrics_ext", env=DEFAULT_ENV,
    )


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task
def nbshell(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Launch a nbshell session.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot python manage.py nbshell",
        env=DEFAULT_ENV,
        pty=True,
    )


@task
def cli(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Launch a bash shell inside the running Nautobot container.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot bash", env=DEFAULT_ENV, pty=True,
    )


@task
def create_user(context, user="admin", nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Create a new user in django (default: admin), will prompt for password.

    Args:
        context (obj): Used to run specific commands
        user (str): name of the superuser to create
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot python manage.py createsuperuser --username {user}",
        env=DEFAULT_ENV,
        pty=True,
    )


@task
def makemigrations(context, name="", nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run Make Migration in Django.

    Args:
        context (obj): Used to run specific commands
        name (str): Name of the migration to be created
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} up -d postgres", env=DEFAULT_ENV,
    )

    if name:
        context.run(
            f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot python manage.py makemigrations --name {name}",
            env=DEFAULT_ENV,
        )
    else:
        context.run(
            f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot python manage.py makemigrations",
            env=DEFAULT_ENV,
        )

    context.run(
        f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} down", env=DEFAULT_ENV,
    )


# ------------------------------------------------------------------------------
# TESTS / LINTING
# ------------------------------------------------------------------------------
@task
def unittest(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run Django unit tests for the plugin.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    docker = f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot"
    context.run(
        f'{docker} sh -c "python manage.py test nautobot_metrics_ext"', env=DEFAULT_ENV, pty=True,
    )


@task
def pylint(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run pylint code analysis.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    docker = f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot"
    # We exclude the /migrations/ directory since it is autogenerated code
    context.run(
        f"{docker} sh -c \"cd /source && find . -name '*.py' -not -path '*/migrations/*' | "
        'PYTHONPATH=/opt/nautobot/netbox xargs pylint"',
        env=DEFAULT_ENV,
        pty=True,
    )


@task
def black(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run black to check that Python files adhere to its style standards.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    docker = f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot"
    context.run(
        f'{docker} sh -c "cd /source && black --check --diff ."', env=DEFAULT_ENV, pty=True,
    )


@task
def pydocstyle(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run pydocstyle to validate docstring formatting adheres to NTC defined standards.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    docker = f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot"
    # We exclude the /migrations/ directory since it is autogenerated code
    context.run(
        f"{docker} sh -c \"cd /source && find . -name '*.py' -not -path '*/migrations/*' | xargs pydocstyle\"",
        env=DEFAULT_ENV,
        pty=True,
    )


@task
def bandit(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run bandit to validate basic static code security analysis.

    Args:
        context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    docker = f"docker-compose -f {COMPOSE_FILE} -p {BUILD_NAME} run nautobot"
    context.run(
        f'{docker} sh -c "cd /source && bandit --recursive ./"', env=DEFAULT_ENV, pty=True,
    )


@task
def tests(context, nautobot_ver=NAUTOBOT_VER, python_ver=PYTHON_VER):
    """Run all tests for this plugin.

    Args:
         context (obj): Used to run specific commands
        nautobot_ver (str): Nautobot version to use to build the container
        python_ver (str): Will use the Python version docker image to build from
    """
    DEFAULT_ENV[NAUTOBOT_VER] = nautobot_ver
    DEFAULT_ENV[PYTHON_VER] = python_ver

    # Sorted loosely from fastest to slowest
    print("Running black...")
    black(context, nautobot_ver=nautobot_ver, python_ver=python_ver)
    print("Running bandit...")
    bandit(context, nautobot_ver=nautobot_ver, python_ver=python_ver)
    print("Running pydocstyle...")
    pydocstyle(context, nautobot_ver=nautobot_ver, python_ver=python_ver)
    print("Running pylint...")
    pylint(context, nautobot_ver=nautobot_ver, python_ver=python_ver)
    print("Running unit tests...")
    unittest(context, nautobot_ver=nautobot_ver, python_ver=python_ver)
    # print("Running yamllint...")
    # yamllint(context, NAME, python_ver)

    print("All tests have passed!")
