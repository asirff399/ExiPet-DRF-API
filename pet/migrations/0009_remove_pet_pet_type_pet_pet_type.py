# Generated by Django 5.1 on 2024-08-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0008_remove_pet_pet_type_pet_pet_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='pet_type',
        ),
        migrations.AddField(
            model_name='pet',
            name='pet_type',
            field=models.ManyToManyField(null=True, to='pet.pettype'),
        ),
    ]
