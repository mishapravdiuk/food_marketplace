# Generated by Django 4.1.4 on 2023-01-27 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_openinghour'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]
