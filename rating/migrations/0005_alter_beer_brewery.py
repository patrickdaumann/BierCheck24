# Generated by Django 4.2 on 2023-04-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0004_alter_beer_brewery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='brewery',
            field=models.CharField(max_length=255),
        ),
    ]
