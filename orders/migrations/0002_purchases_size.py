# Generated by Django 4.2.2 on 2023-06-29 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='size',
            field=models.CharField(default='XL', max_length=100),
            preserve_default=False,
        ),
    ]
