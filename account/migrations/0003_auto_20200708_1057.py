# Generated by Django 3.0.6 on 2020-07-08 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_teammember_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='emp_id',
            field=models.CharField(max_length=12),
        ),
    ]
