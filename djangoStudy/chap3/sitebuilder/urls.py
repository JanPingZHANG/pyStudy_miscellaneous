from django.conf.urls import url
from .views import page
from .views import question

urlpatterns=(
	url(r'^(?P<slug>[\w./-]+)/$',page,name='page'),
	url(r'^$',page,name='homepage'),
	url(r'^mulu/',question,name='question'),
)
