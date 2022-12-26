# Generated by Django 4.1.4 on 2022-12-26 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='accounts.userprofile'),
        ),
    ]
