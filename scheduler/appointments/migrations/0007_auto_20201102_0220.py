# Generated by Django 3.1.2 on 2020-11-02 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_auto_20201101_2205'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('subject', 'start_time', 'end_time')},
        ),
    ]