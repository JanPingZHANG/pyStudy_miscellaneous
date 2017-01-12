import sys
from django.conf import settings
import os
from mulu import GetQuestion

DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY','{{secret_key}}')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')
settings.configure(
	DEBUG = DEBUG,
	SECRET_KEY = SECRET_KEY,
	ROOT_URLCONF = __name__,
	ALLOWED_HOSTS = ALLOWED_HOSTS,
	MIDDLEWARE_CLASS=(
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking,XFrameOptionsMiddleware',
		),
)

from django.conf.urls import url
from django.http import HttpResponse

def index(request):
	return HttpResponse(GetQuestion())

urlpatterns = (
	url(r'^$',index),
	)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
if __name__ == '__main__':
	from django.core.management import execute_from_command_line
	
	execute_from_command_line(sys.argv)
