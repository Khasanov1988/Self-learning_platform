# Generated by Django 4.2.5 on 2023-12-01 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_name_remove_user_surname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.URLField(blank=True, null=True, verbose_name='Profile picture'),
        ),
    ]
