# Generated by Django 5.1.3 on 2024-12-07 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0003_producto_id_unico'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReporteVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venta_id', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_por_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_pagado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cambio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
    ]