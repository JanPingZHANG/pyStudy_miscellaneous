import sys
from django.conf import settings
import os

#DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY','2&xs)x&f6w6b#e@6s*o_vql&aj7%pi&^f-6=&9=*r*7je_sbfq')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')
BASE_DIR = os.path.dirname(__file__)
settings.configure(
	DEBUG = True,
	SECRET_KEY = SECRET_KEY,
	ROOT_URLCONF = 'sitebuilder.urls',
	ALLOWED_HOSTS = ALLOWED_HOSTS,
	MIDDLEWARE_CLASS=(),
	INSTALL_APPS=(
		'django.contrib.staticfiles',
		'sitebuilder',
	),
	TEMPLATES=(
		{
			'BACKEND':'django.template.backends.django.DjangoTemplates',
			'DIRS':(os.path.join(BASE_DIR,'sitebuilder/templates'),),
			'APP_DIRS':True,
		},
	),
	STATIC_URL='/static/',
	SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR,'pages'),
)

if __name__ == '__main__':
	from django.core.management import execute_from_command_line
	
	execute_from_command_line(sys.argv)
