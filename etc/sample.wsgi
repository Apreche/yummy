import sys, site, os

ALLDIRS = [
    '/necessary/paths/here/',
    '/more/necessary/paths/here/',
    '/more/necessary/paths/here/too/',
]
prev_sys_path = list(sys.path)
for directory in ALLDIRS:
    site.addsitedir(directory)
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

from django.core.handlers.wsgi import WSGIHandler
os.environ["DJANGO_SETTINGS_MODULE"] = 'yummy.settings'
os.environ["CELERY_LOADER"] = "django"
application = WSGIHandler()
