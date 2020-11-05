Local Development
=================

.. admonition:: Current State of Documentation

   As the project is currently in its infancy, much of this documentation may be immature and
   quite basic. As the project develops and matures, so too will this documentation, so please
   bear with us in it's current state and feel free to provide a Pull Request to make them better.

We are excited that you want to contribute back to the Glyph project! This document provides an
overview of how to get started with the project from a development standpoint, including the
contribution guidelines, the local development setup, and the different means for deployment of
the application.


Before You Begin
----------------

Before you begin, please read the :doc:`Contribution Guidelines <contributing>` to make your time
working with the project easier for both you and our maintainers. We ask & expect that all
contributions in the form of issues and pull requests follow the formats presented in the guide.


Local Development Setup
-----------------------

In order to begin working with the project locally, the following steps must be adhered to. We will
need to clone the repository locally and set up a virtual environment to run some common, local
commands, and potentially configure for our editor to automatically pick up project tests & linting.

1. Cloning the project
++++++++++++++++++++++

To begin, clone the project to your local machine for development.

.. code-block::
   
   # If using SSH (recommended)
   git clone git@github.com:glyph-community/glyph.git

   # If using HTTPS
   git clone https://github.com/glyph-community/glyph.git

   # If using GitHub CLI
   gh repo clone glyph-community/glyph

2. Environment Configuration
++++++++++++++++++++++++++++

Before running the application, you will need to copy and fill out a ``.env`` file so that the
application can properly connect to any needed services and has the proper local configuration to start.

.. code-block::

   cp .env.example .env


Once copied, open `.env` in your favorite code editor and fill in the missing pieces.

3. Creating a Virtual Environment
+++++++++++++++++++++++++++++++++

It is best practice to use a virtual environment when running Python projects, to avoid dirty-ing
the global interpreter with project-specific dependencies. It provides a nice sandbox to ensure that
the settings / dependencies needed are installed and are the proper versions. This is required
when running ``manage.py`` commands.

To follow these specific steps, you will need ``virtualenv`` installed. The following is how Dan sets
up the virtual environment, feel free to use ``pipenv`` or whatnot if you can get it to work with the
``.vscode/settings.json`` file.

You will then probably want to install the project's dependencies once inside the virtual environment.
This will allow you to run all of the ``manage.py`` commands without worry.

.. code-block::

   virtualenv venv -p python3  # or provide a specific version

   # Activates the virtualenv to be used by the shell session
   source venv/bin/activate

   # install dependencies
   pip install -r requirements/dev_requirements.txt

4. VSCode Integration
+++++++++++++++++++++

The project also has a version-controlled VSCode settings file (``.vscode/settings.json``) that
relies on this ``venv`` directory to exist. It sets the Python interpreter to be ``./venv``
under the project, but it also includes setting custom Pylint arguments to the editor so that it
provides the same configurations as what is run during testing.

Local Operations
----------------

For some core operations - such as database migrations, linting, and test coverage checking - you
can run these through the ``manage.py`` program in the root directory, as you would with a
normal Django project. This requires all of the ``virtualenv`` virtual environment setup as
described above so that the dependencies exist as needed by the scripts.

.. code-block::

   # Run an example `manage.py` command
   ./manage.py makemigrations
   ./manage.py migrate
   ./manage.py test
   ./manage.py lint

   # Runs a local, single-threaded instance
   # of the web server (no workers)
   ./manage.py runserver

Database Operations
+++++++++++++++++++

Getting a database running locally should not be a difficult operation. In local mode - aka when
using ``manage.py`` - Sqlite 3 is used as the database driver, which uses a flat ``.sqlite3``
file under the ``glyph`` directory in the project root as its entire database. This means that
while developing locally, if you ever want to just *start over*, you can simply delete the file.

.. code-block::

   rm glyph/db.sqlite3  # most-likely name & location of the file

To create this file initially though, you will need to run the following while "inside" of the
Python virtual environment:

.. code-block::

   ./manage.py migrate

This will create the database file if it doesn't already exist, and it will perform any **Database 
Migrations** needed to get the database in-sync with what the codebase expects. We highly recommend
you read
`the Django Project's documentation on migrations <https://docs.djangoproject.com/en/3.1/topics/migrations/>`_.

If you make any changes to a model (an app's ``models.py`` file) then you will probably need to
create a new **migration file** so that it can automatically represented in the database correctly.

The can be done with the following command:

.. code-block::

   # creates the actual migration file
   ./manage.py makemigrations

   # If needed, reflect the change(s) in the local db file
   ./manage.py migrate

Note that if using ``docker-compose`` as described below, it is smart enough to automatically
create the database and run migrations needed to get the application to work inside the environment.

Adding Dependencies
+++++++++++++++++++

There are three main files that replace the normal python ``requirements.txt`` file, and they
are all located under the ``requirements`` subdirectory in the project.

* **Documentation** (``documentation.txt``)

  Used for dependencies to generate the documentation, such as ``sphinx`` and any of it's needed extensions.

* **Development & Testing** (``development.txt``)

  Used for all dependencies of the project along with anything needed for project meta, such as
  testing and linting dependencies.

* **Release & Deploy** (``release.txt``)

  Contains a subset of development dependencies that are needed to run the real project in a hosted
  scenario. This file is auto-generated using ``development.txt`` from deps that have the
  ``@DEVONLY`` comment annotation, and by running ``scripts/requirements-gen.py``. This is to
  keep the size of the resulting image & associated container(s) to a minimum.

When adding a dependency, we ask that you ``pip install <whatever>`` it locally, and determine what
the version is using a piped ``grep`` command.

.. code-block::

   $ pip freeze | grep <whatever>
   <whatever>==1.2.3

We ask that you then add only this top-level dependency to either the ``documentation.txt`` or
``development.txt`` file, based on where it is needed. If in ``development.txt``, please add a
comment above the dependency stating what it is for, so that we may know in the future. If a
dependency goes in this file and is only needed for development, and is not required in production,
please include a ``# @DEVONLY`` directly above the dependency.

Notice the example below, where ``django-extensions`` is required during production, and ``flake8``
is only needed during development and testing.

.. code-block::

   # Used to provide common model & manage.py extensions
   django-extensions==3.0.9

   # Used for PEP8 code-checking
   # @DEVONLY
   flake8==3.8.4

.. danger::
   Please never add requirements directly to ``release.txt``! Please add them to ``development.txt``
   and run the generation script given below.

Once ``development.txt`` has been changed, we will need to run the ``scripts/requirements-gen.py``
script to ensure that our production dependencies are up to date.


Docker
------

The project is designed to be easily run in a Docker container and as a complete environment
using ``docker-compose``. While local operations, namely ``manage.py runserver``, can
only run one process at a time, Docker Compose is leveraged to run the entire environment,
including all application components and dependencies in a full-fledged local environment that
can mirror the real world.

.. code-block::

   # Create the entire environment locally inside docker
   docker-compose up --build --remove-orphans

   # When done, you can ctrl-z it to keep data, or
   # you can run the following to really kill everything
   docker-compose down

Note that by default, the Docker Compose environment will use a hybrid of production and development
features, allowing for hot reloading - meaning any code changes instantly get picked up and restart
the server - while still allowing all core components to run in a sandbox environment.

Default Superuser
+++++++++++++++++

When using ``docker-compose``, it will automatically generate a default superuser that can be
logged into. It will create the user on ``docker-compose up`` if it does not already exist in
the database, but **it will not attempt to overwrite any data** on subsequent runs.

The credentials are as follow:

.. code-block::

   Username: dcadmin
   Password: hunter2

Code Style Guide
----------------

Before releases are made or Pull Requests are approved, they must pass PEP8-compatible checks using
``flake8``, a `Python style guide enforcer <https://flake8.pycqa.org/en/latest/index.html>`_.
This will check for syntax errors, but will also ensure that any code in the project follows the
best rules and practices of the Python community, which will ensure a high code quality.

Some major rules to follow:

* Try to provide docstrings for your functions and methods unless it is explicitly private - meaning
  that it starts with an underscore (``_``). This will greatly help the readability of the project.
* The maximum line length in a Python file is 120 characters. If you need to break a string over
  multiple lines, you can wrap it in parentheses and try to make the lines of similar length.
  
  .. code-block:: python

    short_string = 'woohoo, I am short'

    long_string = (
        'Maybe you are looking for a short sentence, or maybe you are looking for a longer string, '
        'but either way, we appreciate you taking the time to read this longer sentence.'
    )

* Single quotes (``'``) are preferred for denoting strings unless it would require an escape, in
  which case double quotes (``"``) are fine.

  .. code-block:: python

     valid = 'hello, world!'
     still_valid = "Don't worry about me!"

     not_valid = "why not single quote me?"

* If you have a long list of arguments and named arguments to a function / method, you can either.

  1. Place them all on one line if they fit
  2. Place all positional arguments on one line and keyword arguments on another if they fit
  3. Place each individual argument on it's own line. 

  In any situation where the call is spanned over multiple lines, the closing parenthesis should be
  indented the same amount as the first line, and the argument lines should be indented one-block,
  most likely being four spaces.

  .. code-block:: python

     single_line_valid = some_function_call(1, 2, c=3)

     multiple_line_condensed = my_obj.method(
         'look_at_my_string', parameter_a, parameter_b,
         check_valid=True, ignore_errors=False
     )

     class SomeModel(models.Model):

         valid_field = models.CharField(
             'Valid Field',
             default='',
             blank=True,
             help_text='This is an example of a valid DB field with each arg on a new line'
         )


Documentation
-------------

Documentation is all located under the ``docs`` directory and is written in reStructuredText
and is compiled to HTML using `Sphinx <https://www.sphinx-doc.org/en/master/>`_. This generated
HTML is then built and managed automatically by `ReadTheDocs.io <https://readthedocs.org/>`_. For a
quick overview of reStructuredText, check out
`this website <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_.
