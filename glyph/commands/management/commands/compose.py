from ..base import AdminCommand


class Command(AdminCommand):
    """
    Tries to make a connection to the database
    This is used by Docker to ensure the database is up and running
    """
    requires_system_checks = False
    help = (
        'Runs the entire application inside of a Docker Compose environment. '
        'Using Ctrl+C will attempt to gracefully stop the containers.'
    )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        args = ['docker-compose', 'up', '--build'] + list(args)
        self.subprocess(args)
