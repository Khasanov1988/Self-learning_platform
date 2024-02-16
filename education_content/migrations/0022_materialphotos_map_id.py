# Generated by Django 4.2.5 on 2024-02-15 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unique_content', '0023_alter_figuremap_map_file'),
        ('education_content', '0021_alter_chapter_description_alter_material_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialphotos',
            name='map_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='unique_content.figuremap', verbose_name='Map'),
        ),
    ]
