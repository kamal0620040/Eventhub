# Generated by Django 3.2 on 2021-05-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20210506_2114'),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='event',
            field=models.ManyToManyField(blank=True, related_name='event', to='events.Event'),
        ),
    ]
