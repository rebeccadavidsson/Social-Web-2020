# Generated by Django 2.2.7 on 2020-03-18 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0012_auto_20200318_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
