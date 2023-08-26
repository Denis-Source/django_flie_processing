# Generated by Django 4.2.3 on 2023-08-26 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('upload', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the task', max_length=24, verbose_name='Name')),
                ('status', models.CharField(choices=[('created', 'Created'), ('running', 'Running'), ('finished', 'Finished'), ('errored', 'Errored'), ('canceled', 'Canceled')], default='created', help_text='Current state of the task', max_length=10, verbose_name='Status')),
                ('created_at', models.DateTimeField(editable=False, help_text='Date that the task was create', verbose_name='Creation date')),
                ('closed_at', models.DateTimeField(blank=True, help_text='Date that the task was finished/errored', null=True, verbose_name='Closure date')),
                ('initiator', models.ForeignKey(help_text='User that initiated the task', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Task initiator')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ConversionTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='task.task')),
                ('output_file', models.FileField(blank=True, help_text='Output File', null=True, upload_to='outputs', verbose_name='Output File')),
                ('output_format', models.CharField(choices=[('blp', 'Blizzard Texture Format'), ('bmp', 'Bitmap'), ('bufr', 'Binary Universal Form for the Representation of meteorological data'), ('dds', 'DirectDraw Surface'), ('dib', 'Device Independent Bitmap'), ('eps', 'Encapsulated PostScript'), ('ps', 'PostScript'), ('grib', 'GRIdded Binary or General Regularly-distributed Information in Binary form'), ('h5', 'Hierarchical Data Format 5'), ('hdf', 'Hierarchical Data Format'), ('icns', 'Apple Icon Image format'), ('ico', 'Icon format'), ('im', 'ImageMagick Script'), ('imt', 'ImageMagick Textual image'), ('jfif', 'JPEG File Interchange Format'), ('jpe', 'JPEG Image'), ('jpeg', 'Joint Photographic Experts Group'), ('jpg', 'JPEG Image'), ('j2c', 'JPEG 2000 Code Stream'), ('j2k', 'JPEG 2000 Image'), ('jp2', 'JPEG 2000 Core Image File'), ('jpc', 'JPEG 2000 Code Stream'), ('jpf', 'JPEG 2000 File Format'), ('jpx', 'JPEG 2000 Part 2'), ('msp', 'Microsoft Paint'), ('pcx', 'PiCture eXchange'), ('apng', 'Animated Portable Network Graphics'), ('png', 'Portable Network Graphics'), ('pbm', 'Portable Bitmap'), ('pgm', 'Portable Graymap'), ('pnm', 'Portable aNy Map'), ('ppm', 'Portable Pixmap'), ('bw', 'SGI Black and White'), ('rgb', 'SGI RGB Image'), ('rgba', 'SGI RGB Image with Alpha Channel'), ('sgi', 'Silicon Graphics Image'), ('icb', 'Truevision Targa Image'), ('tga', 'Truevision TGA Image'), ('vda', 'Truevision Targa Image'), ('vst', 'Truevision Targa Image'), ('tif', 'Tagged Image File Format'), ('tiff', 'Tagged Image File Format'), ('webp', 'WebP image'), ('emf', 'Windows Enhanced Metafile'), ('wmf', 'Windows Metafile'), ('xbm', 'X BitMap'), ('blp', 'Blizzard Texture Format'), ('bmp', 'Bitmap'), ('bufr', 'Binary Universal Form for the Representation of meteorological data'), ('dds', 'DirectDraw Surface'), ('dib', 'Device Independent Bitmap'), ('eps', 'Encapsulated PostScript'), ('ps', 'PostScript'), ('grib', 'GRIdded Binary or General Regularly-distributed Information in Binary form'), ('h5', 'Hierarchical Data Format 5'), ('hdf', 'Hierarchical Data Format'), ('icns', 'Apple Icon Image format'), ('ico', 'Icon format'), ('im', 'ImageMagick Script'), ('imt', 'ImageMagick Textual image'), ('jfif', 'JPEG File Interchange Format'), ('jpe', 'JPEG Image'), ('jpeg', 'Joint Photographic Experts Group'), ('jpg', 'JPEG Image'), ('j2c', 'JPEG 2000 Code Stream'), ('j2k', 'JPEG 2000 Image'), ('jp2', 'JPEG 2000 Core Image File'), ('jpc', 'JPEG 2000 Code Stream'), ('jpf', 'JPEG 2000 File Format'), ('jpx', 'JPEG 2000 Part 2'), ('msp', 'Microsoft Paint'), ('pcx', 'PiCture eXchange'), ('apng', 'Animated Portable Network Graphics'), ('png', 'Portable Network Graphics'), ('pbm', 'Portable Bitmap'), ('pgm', 'Portable Graymap'), ('pnm', 'Portable aNy Map'), ('ppm', 'Portable Pixmap'), ('bw', 'SGI Black and White'), ('rgb', 'SGI RGB Image'), ('rgba', 'SGI RGB Image with Alpha Channel'), ('sgi', 'Silicon Graphics Image'), ('icb', 'Truevision Targa Image'), ('tga', 'Truevision TGA Image'), ('vda', 'Truevision Targa Image'), ('vst', 'Truevision Targa Image'), ('tif', 'Tagged Image File Format'), ('tiff', 'Tagged Image File Format'), ('webp', 'WebP image'), ('emf', 'Windows Enhanced Metafile'), ('wmf', 'Windows Metafile'), ('xbm', 'X BitMap')], max_length=12)),
                ('quality', models.IntegerField(blank=True, default=100, null=True)),
                ('upload', models.ForeignKey(help_text='Uploaded file that need conversion', on_delete=django.db.models.deletion.CASCADE, to='upload.upload', verbose_name='Uploaded file')),
            ],
            bases=('task.task',),
        ),
    ]
