"""
This Pytest configuration file is required so that
VSCode Python test discovery works properly
"""
import os

try:
    from django import setup
    from django.test.runner import DiscoverRunner
except ImportError:
    pass
else:
    runner = DiscoverRunner()
    db_config = None
    def pytest_configure():
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glyph.configuration.settings')
        setup()
        runner.setup_test_environment()
        db_config = runner.setup_databases()

    def pytest_unconfigure():
        if db_config:
            runner.teardown_databases(db_config)
        runner.teardown_test_environment()
