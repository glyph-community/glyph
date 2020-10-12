This is a Django application that provides a common place to write custom Django `manage.py` commands.

The weird `commands/management/commands/*.py` route is a Django-ism since the first `commands` refers to the app,
and then an app can have the subpath `management/commands` where it will try to find the custom admin commands. 

Each file under the `management/commands` directory can be referred by `manage.py <file name without .py>` so
`check_db.py` can be ran as `manage.py check_db`.