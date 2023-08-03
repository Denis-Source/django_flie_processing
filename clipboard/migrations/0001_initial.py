# Generated by Django 4.2.3 on 2023-08-03 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClipBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the clipboard', max_length=32, unique=True, verbose_name='Name')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('other', 'Other')], default='other', help_text='Media type of the clipboard file', max_length=10, verbose_name='Media type')),
                ('file', models.FileField(help_text='Media file', upload_to='clipboards', verbose_name='Media file')),
                ('created_at', models.DateTimeField(blank=True, help_text='Date the clipboard was created at', null=True, verbose_name='Creation date')),
                ('user', models.ForeignKey(help_text='User that uploaded a clipboard', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]