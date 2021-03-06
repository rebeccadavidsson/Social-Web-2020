# Generated by Django 2.2.10 on 2020-03-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0014_auto_20200318_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.CharField(blank=True, default='No interests yet', max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='converter/media/images/logo.png', upload_to='images'),
        ),
    ]
