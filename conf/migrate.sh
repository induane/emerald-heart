#!/bin/bash
echo -e "Running migrations and loading fixtures"
echo $DJANGO_SETTINGS_MODULE
echo $PYTHONPATH
python /emerald_heart/lib/python3.14/site-packages/emerald_heart/manage.py migrate --noinput
python /emerald_heart/lib/python3.14/site-packages/emerald_heart/manage.py loaddata /emerald_heart/lib/python3.14/site-packages/emerald_heart/fixtures/auth.json ||:
python /emerald_heart/lib/python3.14/site-packages/emerald_heart/manage.py loaddata /emerald_heart/lib/python3.14/site-packages/emerald_heart/fixtures/location.json ||:

exit 0
