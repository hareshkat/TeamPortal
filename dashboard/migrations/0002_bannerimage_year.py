# Generated by Django 3.0.6 on 2020-07-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerimage',
            name='year',
            field=models.IntegerField(choices=[(2018, 2018), (2019, 2019), (2020, 2020)], default=2020),
            preserve_default=False,
        ),
    ]
