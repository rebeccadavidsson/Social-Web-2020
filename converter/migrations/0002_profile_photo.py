# Generated by Django 2.2.7 on 2020-02-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='images/logo.png', upload_to='static/images'),
        ),
    ]