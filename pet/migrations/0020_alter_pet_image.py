# Generated by Django 5.1 on 2024-08-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0019_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]
