# Generated by Django 4.2.2 on 2023-06-28 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_category_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]