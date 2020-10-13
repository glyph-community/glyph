import importlib.util
from os import path

spec = importlib.util.spec_from_file_location('load_utils', path.join(path.dirname(__file__), 'load_utils.py'))
load_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load_utils)

command = '/usr/bin/gunicorn'

# Configurable settings
bind = '0.0.0.0:%s' % load_utils.getenv('PORT', int, default=5000)
workers = load_utils.getenv('GUNICORN_WORKERS', int, default=3)
loglevel = 'debug' if load_utils.getenv('DEBUG', bool, default=False) else 'info'

# Send logging to the console
errorlog = load_utils.getenv('GUNICORN_ERROR_LOG', str, default='-')
accesslog = load_utils.getenv('GUNICORN_ACCESS_LOG', str, default='-')
capture_output = errorlog != '-' or accesslog != '-'
