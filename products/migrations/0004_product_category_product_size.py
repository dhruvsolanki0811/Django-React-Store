# Generated by Django 4.2.2 on 2023-06-28 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_category_remove_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('MEN', 'men'), ('WOMEN', 'women'), ('BOYS', 'boys'), ('GIRLS', 'girls')], default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('XL', 'XL'), ('XXL', 'XXL')], default='xl', max_length=100),
            preserve_default=False,
        ),
    ]
