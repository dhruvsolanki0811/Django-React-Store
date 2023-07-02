# Generated by Django 4.2.2 on 2023-07-01 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_delievered'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_payment_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
