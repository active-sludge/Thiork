# Generated by Django 3.2.9 on 2021-12-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thiorkApp', '0004_alter_vectis_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vectis',
            name='photo',
            field=models.ImageField(blank=True, default='ceyda.jpeg', upload_to='profile_photos/%Y/%m/%d/'),
        ),
    ]
