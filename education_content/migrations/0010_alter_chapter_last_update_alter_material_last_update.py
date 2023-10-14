# Generated by Django 4.2.5 on 2023-10-06 12:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0009_alter_material_topic_alter_materialphotos_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='last_update',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Last update date'),
        ),
        migrations.AlterField(
            model_name='material',
            name='last_update',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Last update date'),
        ),
    ]
