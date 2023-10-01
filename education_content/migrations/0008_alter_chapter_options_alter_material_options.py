# Generated by Django 4.2.5 on 2023-10-01 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0007_chapter_is_published_requested_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'permissions': [('set_published', 'Can publish posts')], 'verbose_name': 'Chapter', 'verbose_name_plural': 'Chapters'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'permissions': [('set_published', 'Can publish posts')], 'verbose_name': 'Material', 'verbose_name_plural': 'Materials'},
        ),
    ]
