# Generated by Django 3.2 on 2021-05-03 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20210503_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrule',
            options={'verbose_name_plural': 'Event Rules'},
        ),
        migrations.AlterModelOptions(
            name='eventtype',
            options={'verbose_name_plural': 'Event Types'},
        ),
        migrations.AlterField(
            model_name='event',
            name='event_rule',
            field=models.ManyToManyField(blank=True, to='events.EventRule'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(max_length=100)),
                ('file', models.ImageField(upload_to='')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
