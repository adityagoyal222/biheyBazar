# Generated by Django 3.1.3 on 2020-12-09 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('location', models.PositiveIntegerField(blank=True, choices=[(1, 'Kathmandu'), (2, 'Pokhara'), (3, 'Chitwan'), (4, 'Janakpur'), (5, 'Dang')], null=True)),
                ('culture', models.PositiveIntegerField(blank=True, choices=[(1, 'Brahmin'), (2, 'Newar'), (3, 'Tharu'), (4, 'Terai')], null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic')),
            ],
        ),
    ]
