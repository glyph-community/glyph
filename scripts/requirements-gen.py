#!/usr/bin/env python
import os

DEV_ONLY_ANNOTATION = '@DEVONLY'
REQUIREMENTS_ORIGIN = os.getenv('REQUIREMENTS_ORIGIN', 'requirements/development.txt')
REQUIREMENTS_DEST = os.getenv('REQUIREMENTS_DEST', 'requirements/release.txt')

DEST_HEADING = """AUTO-GENERATED FILE

This file is automatically generated by running `scripts/requirements-gen.py`.
Please do not manually edit this file. You can exclude development-only
requirements by placing a line above the requirement with """ + f'{DEV_ONLY_ANNOTATION} in it.'

if not (REQUIREMENTS_ORIGIN and REQUIREMENTS_DEST):
    raise ValueError('Both origin and destination must be provided.')

cwd = os.getcwd()
if 'scripts' in os.path.basename(cwd):
    cwd = os.path.dirname(cwd)

requirements = []

with open(REQUIREMENTS_ORIGIN, 'r') as origin:
    lines = [line.strip() for line in origin.readlines()]
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if i == 0 or DEV_ONLY_ANNOTATION not in lines[i-1]:
            requirements.append(line)

requirements.sort()

with open(REQUIREMENTS_DEST, 'w') as dest:
    content = '\n'.join(['# ' + line for line in DEST_HEADING.split('\n')])
    content += '\n' + '\n'.join(requirements)
    dest.write(content)