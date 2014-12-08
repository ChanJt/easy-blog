from django.db import models
from taggit.managers import TaggableManager
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
import requests

upload_dir = 'content/BlogPost/%s/%s'

# Create your models here.
class BlogPost(models.Model):
	class Meta:
		ordering = ['-add_date']

	def html_dir(self,filename):
		if self.add_date:
			year = self.add_date.year
		else:
			year = datetime.now().year
		upload_to = upload_dir %(year,filename)
		return upload_to

	title = models.CharField(max_length=100)
	body = models.TextField(blank=True)
	add_date = models.DateTimeField(auto_now_add=True)
	html_file = models.FileField(upload_to=html_dir,blank=True)
	tags = TaggableManager()
	
	def __unicode__(self):
		return self.title

	@property
	def filename(self):
		return self.title if self.title else None

	def get_html(self):
		with open(self.html_file.path) as f:
			return f.read().encode('utf-8')

	def save(self,*args,**kwargs):
		data = ''
		headers = {'Content-Type':'text/plain'}
		if type(self.body)==bytes:
			data = self.body
		elif type(self.body)==unicode:
			data = self.body.encode('utf-8')
		else:
			print 'Error!'
		r = requests.post('https://api.github.com/markdown/raw',headers=headers,data=data)
		self.html_file.save(self.title+'.html',ContentFile(r.text.encode('utf-8')),save=False)
		self.html_file.close()

		super(BlogPost,self).save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('my_blog.views.article',kwargs={'id':self.id})