# Generated by Django 4.2.5 on 2023-12-02 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unique_content', '0005_figurefromp3din_link_for_iframe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mineral',
            name='abbreviation',
            field=models.CharField(max_length=7, verbose_name='Mineral abbreviation'),
        ),
    ]