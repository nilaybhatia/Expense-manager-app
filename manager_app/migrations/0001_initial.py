# Generated by Django 2.2.6 on 2019-10-07 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('contact_no', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('labour_hours_per_month', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Savings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0.0)),
                ('date_saved', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('INSURANCE', 'To insurance provider'), ('RD', 'Recurring deposit'), ('FD', 'Fixed deposit'), ('INVESTMENT', 'Investment'), ('OTHERS', 'Others')], max_length=30)),
                ('comments', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Savings',
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('source', models.CharField(choices=[('JOB', 'From Job salary'), ('RENT', 'From house rent'), ('POLICY', 'From policy benefit'), ('STOCKS', 'Return on investment in stocks'), ('OTHERS', 'Others')], max_length=20)),
                ('date_received', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_taxed', models.BooleanField(default=False)),
                ('is_major', models.BooleanField(default=False)),
                ('comments', models.TextField()),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.Organisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0.0)),
                ('date_spent', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('NECESSITY', 'Necessity'), ('LEISURE', 'Leisure'), ('OTHERS', 'Others')], max_length=30)),
                ('comments', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
