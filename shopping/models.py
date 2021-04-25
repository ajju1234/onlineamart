

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Cart(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	create_date = models.DateTimeField(verbose_name='create date', auto_now=True)
	checked_out = models.BooleanField(default=False, verbose_name='checked out')

	def __unicode__(self):
		return str(self.create_date)

class Product(models.Model):
	title = models.CharField(null=True, blank=True, max_length=100)
	description = models.CharField(null=True, blank=True, max_length=100)
	unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name = 'unit price')
	total_items = models.IntegerField()
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.title

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Item(models.Model):
	cart = models.ForeignKey(Cart, verbose_name='cart', related_name='cart', on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField(verbose_name='quantity')
	product = models.ForeignKey(Product, verbose_name='product', related_name='product', on_delete = models.CASCADE)

	def __unicode__(self):
		return '%d units' % (self.quantity)

class Review(models.Model):
	rating_choices=[
		(1, 'Very Poor'),
		(2, 'Bad'),
		(3, 'Average'),
		(4, 'Good'),
		(5, 'Very Good')
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product=models.ForeignKey(Product, on_delete=models.CASCADE)
	rating=models.IntegerField(choices=rating_choices)
	review_text=models.CharField(max_length=300, null=True, blank=True)
	review_date=models.DateTimeField(auto_now=True)