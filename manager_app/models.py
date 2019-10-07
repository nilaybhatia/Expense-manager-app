from django.db import models

# Create your models here.
class Income(models.Model):
	user = models.ForeignKey()
	value = models.FloatField()
	source = models.CharField(choices=)
	date_received = models.DateTimeField()
	is_taxed = models.BooleanField()
	is_major = models.BooleanField()
	organisation = models.ForeignKey(Organisation)
	comments = models.TextField()

class Orgaisation(models.Model):
	name = CharField()
	address = TextField()
	contact_no = PhoneNumberField()
	email = EmailField()
	labour_hours_per_month = SmallPositiveIntegerField()

class  Savings():
	user=models.ForeignKey()
	value = models.FloatField()
	date_saved = models. DateTimeField()
	category = models.ChaField()
	comments = TextField

class Expenditure():
	user = models.ForeignKey()
	value = models.FoatField()
	date_spent = models.DateTimeField()
	category = models.CharField()
	comments = models.TextField()
