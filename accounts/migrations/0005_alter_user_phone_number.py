# Generated by Django 4.1.4 on 2023-01-30 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_address_line_1_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
