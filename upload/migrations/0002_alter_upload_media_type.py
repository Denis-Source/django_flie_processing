# Generated by Django 4.2.3 on 2023-08-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('other', 'Other')], default='other', editable=False, help_text='Media type of the upload file', max_length=10, verbose_name='Media type'),
        ),
    ]