# Generated by Django 4.2.5 on 2024-02-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0020_materialphotos_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description'),
        ),
    ]