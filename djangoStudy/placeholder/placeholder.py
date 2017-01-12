import sys
from django.conf import settings
import os
from django.core.cache import cache
from django.views.decorators.http import etag
import hashlib
from django.conf.urls import url
from django.http import HttpResponse,HttpResponseBadRequest
from django import forms
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line
from django.core.urlresolvers import reverse
from django.shortcuts import render


DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY','t(2i7(m^8m!p9=et39f#uo3c0cg=8nt=1r_8p=qb#qz$woi885')
BASE_DIR = os.path.dirname(__file__)
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
	INSTALLED_APPS=('django.contrib.staticfiles',),
	TEMPLATES=(
		{
		'BACKEND':'django.template.backends.django.DjangoTemplates',
		'DIRS':(os.path.join(BASE_DIR,'templates'),),
		},
	),
	STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),),
	STATIC_URL='/static/',
)

def index(request):
	example = reverse('placeholder',kwargs={'width':50,'height':50})
	context = {'example':request.build_absolute_uri(example)}
	return render(request,'home.html',context)

class ImageForm(forms.Form):
	"""Form to validate requested placeholder image."""
	height = forms.IntegerField(min_value=1,max_value=2000)
	width = forms.IntegerField(min_value=1,max_value=2000)
	def generate(self,image_format='PNG'):
		"""Generate an image of the given type and return as raw bytes."""
		height = self.cleaned_data['height']
		width = self.cleaned_data['width']
		print 'generate a new image width: ',width,' height: ',height
		key = '{}.{}.{}'.format(height,width,image_format)
		content = cache.get(key)
		if content is None:
			print 'create a new image width: ',width,' height: ',height
			image = Image.new('RGB',(width,height))
			draw = ImageDraw.Draw(image)
			text = '{0} X {1}'.format(width,height)
			textWidth,textHeight = draw.textsize(text)
			if textWidth<width and textHeight < height:
				texttop = (height - textHeight) // 2
				textleft = (width - textWidth) // 2
				draw.text((textleft,texttop),text,fill=(255,255,255))
			content = BytesIO()
			image.save(content,image_format)
			content.seek(0)
			cache.set(key,content,60*60)
		return content


def generate_etag(request,width,height):
	content = 'Placeholder: {0} x {1}'.format(width,height)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag) 
def placeholder(request,width,height):
	form = ImageForm({'height':height,'width':width})
	if form.is_valid():
		image = form.generate()
		height = form.cleaned_data['height']
		width = form.cleaned_data['width']
		return HttpResponse(image,content_type='image/png')
	else:
		return HttpResponseBadRequest('invalid image request')

urlpatterns = (
	url(r'image/(?P<width>[0-9]+)x(?P<height>[0-9]+)',placeholder,name='placeholder'),
	url(r'^$',index,name='homepage'),
	)

application = get_wsgi_application()
if __name__ == '__main__':
		
	execute_from_command_line(sys.argv)
