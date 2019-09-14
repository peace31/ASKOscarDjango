#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ask_Oskar.settings")

    from django.core.management import execute_from_command_line

    if (sys.argv.__len__() == 1):
        sys.argv.append('runserver')
    print(sys.argv)
    execute_from_command_line(sys.argv)
