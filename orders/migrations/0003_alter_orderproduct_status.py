# Generated by Django 4.1 on 2022-10-09 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('confirmed', 'confrimed'), ('shipped', 'shipped'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered')], default='New', max_length=100),
        ),
    ]
