from django.db import models
from django.conf import settings
from django.utils import timezone
from phone_field import PhoneField
# Create your models here.

class Organisation(models.Model):
	name = models.CharField(max_length=30)
	address = models.TextField()
	contact_no = PhoneField(blank=True, help_text = 'Contact phone number')
	email = models.EmailField(blank=True)
	labour_hours_per_month = models.PositiveSmallIntegerField()
	def __str__(self):
		return self.name

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
	source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
	date_received = models.DateField(default=timezone.now)
	is_taxed = models.BooleanField(default=False)
	is_major = models.BooleanField(default=False)
	organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
	comments = models.TextField()
	def __str__(self):
		return self.user.username+str(self.date_received)


class Savings(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	value = models.FloatField(default=0.0)
	date_saved = models.DateField(default=timezone.now)
	CATEGORY_CHOICES=[
		('INSURANCE', 'To insurance provider'), 
		('RD', 'Recurring deposit'), 
		('FD', 'Fixed deposit'), 
		('INVESTMENT', 'Investment'), 
		('OTHERS', 'Others'),
	]
	category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
	comments = models.TextField()
	class Meta:
		verbose_name_plural = "Savings"
	def __str__(self):
		return self.user.username+str(self.date_saved)


class Expenditure(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	value = models.FloatField(default=0.0)
	date_spent = models.DateField(default=timezone.now)
	CATEGORY_CHOICES=[
		('NECESSITY', 'Necessity'), 
		('LEISURE', 'Leisure'), 
		('OTHERS', 'Others'), 
	]
	category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
	comments = models.TextField()
	def __str__(self):
		return self.user.username+str(self.date_spent)
