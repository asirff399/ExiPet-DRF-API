# Generated by Django 5.1 on 2024-08-20 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0010_alter_pet_pet_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
