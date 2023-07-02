# Generated by Django 4.2.2 on 2023-06-28 06:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='orders.order', to_field='order_id')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_name', to='products.product', to_field='name')),
            ],
        ),
    ]
