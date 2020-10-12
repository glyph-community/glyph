import os
import subprocess

from django.conf import settings

from ..base import AdminCommand

class Command(AdminCommand):
    """
    Tries to make a connection to the database
    This is used by Docker to ensure the database is up and running
    """
    requires_system_checks = False

    DOCS_SUBDIRECTORY = 'docs'

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, default='docs')
        parser.add_argument('--sphinx-build', type=str, default=os.getenv('SPHINXBUILD', 'sphinx-build'))
        parser.add_argument('--source-dir', type=str, default=os.getenv('SOURCEDIR', 'source'))
        parser.add_argument('--build-dir', type=str, default=os.getenv('BUILDDIR', 'build'))

    def handle(self, *args, **options):
        args = list(args)
        output_type = args.pop(0) if args else 'html'
        subdir = options['dir']
        os.chdir(subdir)
        cmd = options['sphinx_build']

        build = options['build_dir']
        real_output = os.path.join(build, 'html')
        doctrees = os.path.join(build, '.doctrees')

        args = [cmd, f'-b={output_type}', f'-d={doctrees}', '-W', options['source_dir'], real_output] + args
        self.info(f'$> "{args}"')
        p = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, b''):
            self.info(line.decode('utf-8'))
        p.stdout.close()
        p.wait()
