# Generated by Django 3.1.3 on 2020-12-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='review_int',
            field=models.IntegerField(default=0),
        ),
    ]
