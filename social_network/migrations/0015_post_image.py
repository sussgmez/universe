# Generated by Django 5.1.6 on 2025-03-03 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0014_alter_profile_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/post', verbose_name='Imagen'),
        ),
    ]
