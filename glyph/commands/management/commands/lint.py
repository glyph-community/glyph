from ..base import AdminCommand


class Command(AdminCommand):
    """
    Tries to make a connection to the database
    This is used by Docker to ensure the database is up and running
    """
    requires_system_checks = False
    help = 'Run flake8 against the application to check for syntax and style errors.'

    def add_arguments(self, parser):
        parser.add_argument('--syntax', action='store_true')

    def handle(self, *args, **options):
        flake_args = ['flake8', 'glyph', '--statistics', '--count']
        if options['syntax']:
            self.info('Syntax checking...')
            flake_args += ['--exit-zero', '--max-complexity=10']
        else:
            self.info('Style checking...')
            flake_args += ['--select=E9,F63,F7,F82', '--show-source']
        self.subprocess(flake_args)
