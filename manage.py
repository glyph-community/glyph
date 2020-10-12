#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

COVERAGE_COMMANDS = ['test']

# Load from .env if it exists
load_dotenv()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glyph.configuration.settings')

    is_testing = any(map(lambda arg: arg in sys.argv, COVERAGE_COMMANDS))
    if is_testing:
        import coverage
        cov = coverage.coverage(
            source=['glyph'],
            config_file='.coveragerc',
        )
        cov.erase()
        cov.start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        try:
            cov.report()
            cov.html_report(directory='htmlcov')
        except coverage.misc.CoverageException as e:
            if 'No data to report' not in str(e):
                raise e


if __name__ == '__main__':
    main()
