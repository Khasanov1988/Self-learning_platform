# Generated by Django 4.2.5 on 2023-10-13 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0010_alter_chapter_last_update_alter_material_last_update'),
        ('tests', '0003_completedquestion_completed_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completedquestion',
            options={'verbose_name': 'Completed Question', 'verbose_name_plural': 'Completed Questions'},
        ),
        migrations.AlterField(
            model_name='test',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_content.material', unique=True),
        ),
    ]