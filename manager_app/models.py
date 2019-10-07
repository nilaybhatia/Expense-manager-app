from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Income(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	value = models.FloatField()
	SOURCE_CHOICES=[
		('JOB', 'From Job salary'), 
		('RENT', 'From house rent'), 
		('POLICY', 'From policy benefit'), 
		('STOCKS', 'Return on investment in stocks'), 
		('OTHERS', 'Others'),
	]
	source = models.CharField(max_lenght=20, choices=SOURCE_CHOICES)
	date_received = models.DateTimeField(default=timezone.now)
	is_taxed = models.BooleanField(default=False)
	is_major = models.BooleanField(default=False)
	organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
	comments = models.TextField()
	def __str__(self):
		return self.username

class Orgaisation(models.Model):
	name = CharField(max_length=30)
	address = TextField()
	contact_no = PhoneField(blank=True, help_text = 'Contact phone number')
	email = EmailField()
	labour_hours_per_month = SmallPositiveIntegerField()
	def __str__(self):
		return self.name

class Savings():
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
	value = models.FloatField()
	date_saved = models.DateTimeField(default=timezone.now)
	CATEGORY_CHOICES=[
		('INSURANCE', 'To insurance provider'), 
		('RD', 'Recurring deposit'), 
		('FD', 'Fixed deposit'), 
		('INVESTMENT', 'Investment'), 
		('OTHERS', 'Others'),
	]
	category = models.CharField(max_length=30, choice=CATEGORY_CHOICES)
	comments = TextField()

class Expenditure():
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	value = models.FoatField()
	date_spent = models.DateTimeField(default=timezone.now)
	CATEGORY_CHOICES=[
		('NECESSITY', 'Necessity'), 
		('LEISURE', 'Leisure'), 
		('OTHERS', 'Others'), 
	]
	category = models.CharField()
	comments = models.TextField()
