# Generated by Django 3.2 on 2021-05-06 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20210506_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='events.event'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='event_photos'),
        ),
    ]
